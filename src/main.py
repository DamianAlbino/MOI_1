import os
import sys
import pandas as pd
from ortools.linear_solver import pywraplp


os.chdir(os.getcwd())

def load_data(file_path):
    """ Carga los datos desde un archivo Excel especificado. """

    sheets = ["Plants", "Suppliers", "Clients", "Periods", "Products", 
              "Production_costs", "Purchase_costs", "Storage_costs", 
              "Sales_revenue", "Production_time", "Production_capacity", 
              "Client_demand", "Initial_inventory", "Max_purchase_budget"]
    
    data = {sheet: pd.read_excel(file_path, sheet_name=sheet) for sheet in sheets}
    return data

def create_dict_from_df(df, index_cols, value_col):
    """ Crea un diccionario a partir de columnas especificadas en un DataFrame. """
    return dict(zip(df[index_cols].apply(tuple, axis=1), df[value_col]))

def initialize_solver():
    """ Inicializa y devuelve un objeto Solver de OR-Tools. """
    return pywraplp.Solver.CreateSolver('SCIP')

def build_model(data, solver):
    # Definición de conjuntos y parámetros
    I = data['Plants']['Plant'].unique().tolist()
    J = data['Suppliers']['Supplier'].unique().tolist()
    K = data['Clients']['Client'].unique().tolist()
    T = ['Periodo 0'] + data['Periods']['Period'].unique().tolist()  # Añadimos Periodo 0
    P = data['Products']['Product'].unique().tolist()
    
    # Diccionarios de costos y otros parámetros
    c = create_dict_from_df(data['Production_costs'], ['Plant', 'Product'], 'Cost')
    d = create_dict_from_df(data['Purchase_costs'], ['Supplier', 'Plant', 'Product', 'Period'], 'Cost')
    h = create_dict_from_df(data['Storage_costs'], ['Plant', 'Product'], 'Cost')
    e = create_dict_from_df(data['Sales_revenue'], ['Plant', 'Client', 'Product', 'Period'], 'Revenue')
    q = create_dict_from_df(data['Production_time'], ['Plant', 'Product'], 'Time')
    Q = create_dict_from_df(data['Production_capacity'], ['Plant', 'Period'], 'Capacity')
    Y = float(data['Max_purchase_budget']['Y'].values[0])
    D = create_dict_from_df(data['Client_demand'], ['Client', 'Product', 'Period'], 'Demand')
    initial_inventory = create_dict_from_df(data['Initial_inventory'], ['Plant', 'Product'], 'Inventory')

    # Variables de decisión
    x, y, z, s = {}, {}, {}, {}
    for i in I:
        for p in P:
             # Obtener el valor del inventario inicial para la planta i y el producto p
            initial_inv = initial_inventory.get((i, p), 0)  # Usamos .get() para manejar casos sin inventario inicial
            # Fijar el inventario inicial en el Periodo 0 a ese valor específico
            s[(i, p, T[0])] = solver.IntVar(initial_inv, initial_inv, f's_{i}_{p}_{T[0]}')
            for t in T[1:]:  # Empezamos en 1 para saltar 'Periodo 0' para otras variables
                x[(i, p, t)] = solver.IntVar(0, solver.infinity(), f'x_{i}_{p}_{t}')
                s[(i, p, t)] = solver.IntVar(0, solver.infinity(), f's_{i}_{p}_{t}')
                for j in J:
                    y[(j, i, p, t)] = solver.IntVar(0, solver.infinity(), f'y_{j}_{i}_{p}_{t}')
                for k in K:
                    z[(i, k, p, t)] = solver.IntVar(0, solver.infinity(), f'z_{i}_{k}_{p}_{t}')

    # Integración de las restricciones:
    # Restricciones de balance de inventario
    for i in I:
        for p in P:
            for t_idx, t in enumerate(T[1:], start=1):  # Comienza en el primer periodo real
                # Balance de inventario en periodos subsiguientes
                constraint = solver.Constraint(0, 0)
                constraint.SetCoefficient(s[(i, p, t)], 1)
                constraint.SetCoefficient(s[(i, p, T[t_idx-1])], -1)
                constraint.SetCoefficient(x[(i, p, t)], -1)
                for j in J:
                    constraint.SetCoefficient(y[(j, i, p, t)], -1)
                for k in K: 
                    constraint.SetCoefficient(z[(i, k, p, t)], 1)

    # Restricciones de capacidad de producción
    for i in I:
        for t in T[1:]:  # Comenzamos en 1 para saltar 'Periodo 0'
            constraint = solver.Constraint(0, Q[(i, t)])
            for p in P:
                constraint.SetCoefficient(x[(i, p, t)], q[(i, p)])

    # Restricciones de demanda de clientes
    for k in K:
        for p in P:
            for t in T[1:]:  # Saltamos 'Periodo 0'
                constraint = solver.Constraint(0, D[(k, p, t)])
                for i in I:
                    constraint.SetCoefficient(z[(i, k, p, t)], 1)
               
    # Restricciones de capacidad de oferta de plantas
    for i in I:
        for k in K:
            for p in P:
                for t_idx, t in enumerate(T[1:], start=1):  # Empezamos desde 'Periodo 1'
                    constraint = solver.Constraint(0, solver.infinity())
                    # Usamos T[t_idx-1] que correctamente se refiere al período anterior sin salirnos del rango
                    constraint.SetCoefficient(s[(i, p, T[t_idx-1])], 1)
                    constraint.SetCoefficient(x[(i, p, t)], 1)
                    for j in J:
                        constraint.SetCoefficient(y[(j, i, p, t)], 1)
                    constraint.SetCoefficient(z[(i, k, p, t)], -1)
 
    # Restricciones de compra máxima
    constraint = solver.Constraint(0, Y)
    for i in I:
        for j in J:
            for p in P:
                for t in T[1:]:  # Excluimos el 'Periodo 0' para compras
                    constraint.SetCoefficient(y[(j, i, p, t)], d[(j, i, p, t)])

    # Función objetivo: Maximizar rentabilidad
    objective = solver.Objective()
    for k in K:
        for i in I:
            for p in P:
                for t in T[1:]:  # Excluimos el 'Periodo 0'
                    objective.SetCoefficient(z[(i, k, p, t)], e[(i, k, p, t)])  # Ingreso por ventas
                    objective.SetCoefficient(x[(i, p, t)], -c[(i, p)])          # Costo de producción
                    objective.SetCoefficient(s[(i, p, t)], -h[(i, p)])          # Costo de almacenamiento
                    for j in J:
                        objective.SetCoefficient(y[(j, i, p, t)], -d[(j, i, p, t)])  # Costo de compra y transporte
    objective.SetMaximization()
    
    solver.Solve()
    first_objective_value = solver.Objective().Value()

    for i in I:
        for p in P:
            for t in T[1:]:
                x[(i, p, t)]
                for j in J:
                    y[(j, i, p, t)]
                for k in K:
                    z[(i, k, p, t)]

    # Primer función objetivo como restricción
    constraint = solver.Constraint(0.8* first_objective_value, solver.infinity())
    for k in K:
        for i in I:
            for p in P:
                for t in T[1:]:  # Excluimos el 'Periodo 0'
                    constraint.SetCoefficient(z[(i, k, p, t)], e[(i, k, p, t)])  # Ingreso por ventas
                    constraint.SetCoefficient(x[(i, p, t)], -c[(i, p)])          # Costo de producción
                    constraint.SetCoefficient(s[(i, p, t)], -h[(i, p)])          # Costo de almacenamiento
                    for j in J:
                        constraint.SetCoefficient(y[(j, i, p, t)], -d[(j, i, p, t)])  # Costo de compra y transporte

    # Función objetivo: Maximizar demanda satisfecha
    objective.Clear()
    for k in K:
        for i in I:
            for p in P:
                for t in T[1:]:
                    objective.SetCoefficient(z[(i, k, p, t)], 1)  # Producto vendido
    objective.SetMaximization()

    # Devolver el solver y las variables y conjuntos necesarios
    return solver, I, J, K, P, T, x, y, z, s, c, d, h, e

def solve_model(solver, I, J, K, P, T, x, y, z, s, c, d, h, e):
    """ Resuelve el modelo y imprime resultados óptimos incluyendo el valor de la función objetivo. """
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        # Evaluar el valor de la primera función objetivo con la solución actual
        first_objective_value = sum(e[(i, k, p, t)] * z[(i, k, p, t)].solution_value() for k in K for i in I for p in P for t in T[1:]) - sum(c[(i, p)] * x[(i, p, t)].solution_value() + h[(i, p)] * s[(i, p, t)].solution_value() for i in I for p in P for t in T[1:]) - sum(d[(j, i, p, t)] * y[(j, i, p, t)].solution_value() for j in J for i in I for p in P for t in T[1:])
        print(f'Valor de la primera función objetivo: ${first_objective_value:,.2f}')

        # Valor actual de la función objetivo (segunda optimización)
        print(f'Valor de la segunda función objetivo: {solver.Objective().Value():,.0f}')
        # Imprimir los valores de las variables de decisión que no son cero
        for i in I:
            for p in P:
                for t in T[1:]:
                    if x[(i, p, t)].solution_value() != 0:
                        print(f'x[{i},{p},{t}] = {x[(i, p, t)].solution_value():,.0f}')
        for i in I:
            for p in P:
                for t in T[1:]:
                    for j in J:
                        if y[(j, i, p, t)].solution_value() != 0:
                            print(f'y[{j},{i},{p},{t}] = {y[(j, i, p, t)].solution_value():,.0f}')
        for i in I:
            for k in K:
                for p in P:
                    for t in T[1:]:
                        if z[(i, k, p, t)].solution_value() != 0:
                            print(f'z[{i},{k},{p},{t}] = {z[(i, k, p, t)].solution_value():,.0f}')
        for i in I:
            for p in P:
                for t in T[1:]:
                    if s[(i, p, t)].solution_value() != 0:
                        print(f's[{i},{p},{t}] = {s[(i, p, t)].solution_value():,.0f}')

    elif status == pywraplp.Solver.FEASIBLE:
        print('Solución factible encontrada, pero no necesariamente óptima.')
        print(f'Valor de la función objetivo (factible): {solver.Objective().Value()}')
    else:
        print('No se encontró una solución factible o hubo algún otro error.')

def main(file_path):
    data = load_data(file_path)
    solver = initialize_solver()
    
    # Asegurarse de que build_model devuelve tanto el solver como las variables y conjuntos necesarios
    solver, I, J, K, P, T, x, y, z, s, c, d, h, e = build_model(data, solver)
    
    # Pasar todos los parámetros necesarios a solve_model
    solve_model(solver, I, J, K, P, T, x, y, z, s, c, d, h, e)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: No se especificó el archivo de datos.")
    else:
        main(sys.argv[1])