import pandas as pd

# Creando DataFrames
# Definición de los conjuntos como DataFrames
plants = pd.DataFrame({'Plant': ['PlantaA', 'PlantaB']})
suppliers = pd.DataFrame({'Supplier': ['ProveedorA', 'ProveedorB']})
clients = pd.DataFrame({'Client': ['ClienteA', 'ClienteB']})
periods = pd.DataFrame({'Period': ['Semestre1', 'Semestre2']})
products = pd.DataFrame({'Product': ['Artículo1', 'Artículo2']})

# Costos de producción por planta y producto
production_costs = pd.DataFrame({
    'Plant': ['PlantaA', 'PlantaA', 'PlantaB', 'PlantaB'],
    'Product': ['Artículo1', 'Artículo2', 'Artículo1', 'Artículo2'],
    'Cost': [5, 8, 10, 4]
})

# Costos de compra incluyendo envío de proveedor a planta por producto y período
purchase_costs = pd.DataFrame({
    'Supplier': ['ProveedorA','ProveedorA','ProveedorA','ProveedorA','ProveedorA','ProveedorA','ProveedorA','ProveedorA', 'ProveedorB','ProveedorB','ProveedorB','ProveedorB','ProveedorB','ProveedorB','ProveedorB','ProveedorB'],
    'Plant': ['PlantaA', 'PlantaA', 'PlantaA', 'PlantaA', 'PlantaB', 'PlantaB', 'PlantaB', 'PlantaB','PlantaA', 'PlantaA', 'PlantaA', 'PlantaA', 'PlantaB', 'PlantaB', 'PlantaB', 'PlantaB'],
    'Product': ['Artículo1', 'Artículo2', 'Artículo1', 'Artículo2', 'Artículo1', 'Artículo2', 'Artículo1', 'Artículo2', 'Artículo1', 'Artículo2', 'Artículo1', 'Artículo2', 'Artículo1', 'Artículo2', 'Artículo1', 'Artículo2'],
    'Period': ['Semestre1', 'Semestre1', 'Semestre2', 'Semestre2', 'Semestre1', 'Semestre1', 'Semestre2', 'Semestre2', 'Semestre1', 'Semestre1', 'Semestre2', 'Semestre2', 'Semestre1', 'Semestre1', 'Semestre2', 'Semestre2'],
    'Cost': [15,20,8,12,13,17,11,13,12,9,9,10,13,12,12,11]
})

# Costos de almacenamiento por planta y producto
storage_costs = pd.DataFrame({
    'Plant': ['PlantaA', 'PlantaA', 'PlantaB', 'PlantaB'],
    'Product': ['Artículo1', 'Artículo2', 'Artículo1', 'Artículo2'],
    'Cost': [3, 1, 2, 2]
})

# Ingresos netos por ventas de planta a cliente por producto y período
sales_revenue = pd.DataFrame({
    'Plant': ['PlantaA', 'PlantaA', 'PlantaA', 'PlantaA', 'PlantaA', 'PlantaA', 'PlantaA', 'PlantaA', 'PlantaB', 'PlantaB', 'PlantaB', 'PlantaB', 'PlantaB', 'PlantaB', 'PlantaB', 'PlantaB'],
    'Client': ['ClienteA', 'ClienteA', 'ClienteA', 'ClienteA', 'ClienteB', 'ClienteB', 'ClienteB', 'ClienteB', 'ClienteA', 'ClienteA', 'ClienteA', 'ClienteA', 'ClienteB', 'ClienteB', 'ClienteB', 'ClienteB'],
    'Product': ['Artículo1', 'Artículo2', 'Artículo1', 'Artículo2', 'Artículo1', 'Artículo2', 'Artículo1', 'Artículo2', 'Artículo1', 'Artículo2', 'Artículo1', 'Artículo2', 'Artículo1', 'Artículo2', 'Artículo1', 'Artículo2'],
    'Period': ['Semestre1', 'Semestre1', 'Semestre2', 'Semestre2', 'Semestre1', 'Semestre1', 'Semestre2', 'Semestre2', 'Semestre1', 'Semestre1', 'Semestre2', 'Semestre2', 'Semestre1', 'Semestre1', 'Semestre2', 'Semestre2'],
    'Revenue': [12, 11, 11, 12, 10, 10, 12, 11, 11, 12, 10, 10, 12, 11, 11, 12]
})

# Tiempo requerido para producir cada producto en cada planta
production_time = pd.DataFrame({
    'Plant': ['PlantaA', 'PlantaA', 'PlantaB', 'PlantaB'],
    'Product': ['Artículo1', 'Artículo2', 'Artículo1', 'Artículo2'],
    'Time': [2, 1, 1, 2]
})

# Capacidad máxima de tiempo de producción en cada planta por periodo
production_capacity = pd.DataFrame({
    'Plant': ['PlantaA', 'PlantaA', 'PlantaB', 'PlantaB'],
    'Period': ['Semestre1', 'Semestre2', 'Semestre1', 'Semestre2'],
    'Capacity': [90, 120, 100, 130]
})

# Demanda mínima de cada cliente por producto y periodo
client_demand = pd.DataFrame({
    'Client': ['ClienteA', 'ClienteA', 'ClienteA', 'ClienteA', 'ClienteB', 'ClienteB', 'ClienteB', 'ClienteB'],
    'Product': ['Artículo1', 'Artículo1', 'Artículo2', 'Artículo2', 'Artículo1', 'Artículo1', 'Artículo2', 'Artículo2'],
    'Period': ['Semestre1', 'Semestre2', 'Semestre1', 'Semestre2', 'Semestre1', 'Semestre2', 'Semestre1', 'Semestre2'],
    'Demand': [130, 90, 100, 120, 120, 100, 90, 130]})

# Inventario inicial por planta y producto
Initial_inventory = pd.DataFrame({
    'Plant': ['PlantaA', 'PlantaA', 'PlantaB', 'PlantaB'],
    'Product': ['Artículo1', 'Artículo2', 'Artículo1', 'Artículo2'],
    'Inventory': [5, 10, 10, 5]
})

# Presupuesto máximo de compra
Max_purchase_budget = pd.DataFrame({'Y': [9999999999999]})

with pd.ExcelWriter(r"..\test\data.xlsx") as writer:
    plants.to_excel(writer, sheet_name='Plants', index=False)
    suppliers.to_excel(writer, sheet_name='Suppliers', index=False)
    clients.to_excel(writer, sheet_name='Clients', index=False)
    periods.to_excel(writer, sheet_name='Periods', index=False)
    products.to_excel(writer, sheet_name='Products', index=False)
    production_costs.to_excel(writer, sheet_name='Production_costs', index=False)
    purchase_costs.to_excel(writer, sheet_name='Purchase_costs', index=False)
    storage_costs.to_excel(writer, sheet_name='Storage_costs', index=False)
    sales_revenue.to_excel(writer, sheet_name='Sales_revenue', index=False)
    production_time.to_excel(writer, sheet_name='Production_time', index=False)
    production_capacity.to_excel(writer, sheet_name='Production_capacity', index=False)
    client_demand.to_excel(writer, sheet_name='Client_demand', index=False)
    Initial_inventory.to_excel(writer, sheet_name='Initial_inventory', index=False)
    Max_purchase_budget.to_excel(writer, sheet_name='Max_purchase_budget', index=False)