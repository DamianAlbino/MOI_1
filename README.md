# Proyecto de Optimización de Cadena de Suministro

### Damián Jacob Albino Mejía A01246716

## Descripción del Proyecto
Este proyecto implementa un modelo de optimización de la cadena de suministro utilizando programación lineal con la biblioteca de optimización OR-Tools. El modelo está diseñado para maximizar la rentabilidad determinando los planes de producción, almacenamiento, compra y transporte que maximizan los ingresos mientras minimizan los costos asociados.

## Estructura de Archivos
- `documents/`: Contiene el PDF del problema modelado.
  - `Modelo_Matematico_Planeacion.pdf`: El documento explicatorio del modelo implementado.
- `src/`: Directorio de los códigos fuente.
  - `main.py`: El script principal que ejecuta el modelo de optimización.
  - `data_test.py`: Script para probar la carga y manejo de datos.
- `test/`: Contiene el archivo de prueba.
- `.gitignore`: Especifica los archivos que git debe ignorar.
- `requirements.txt`: Enumera todas las dependencias de Python necesarias para el proyecto.

## Cómo Empezar
Para ejecutar este proyecto, asegúrese de tener Python instalado en su sistema y siga los pasos a continuación:

1. Clone el repositorio en su máquina local.
2. Navegue hasta el directorio del proyecto y cree un entorno virtual: `python -m venv venv`
3. Active el entorno virtual:
- En Windows: `venv\Scripts\activate`
- En Unix o MacOS: `source venv/bin/activate`
4. Instale las dependencias del proyecto: `pip install -r requirements.txt`
5. Ejecute el script del archivo de prueba si no lo ha descargado: `python src/data_test.py`
6. Ejecute el script principal pasando la ruta al archivo de datos como argumento: `python src/main.py test/data.xlsx`



## Uso del Código
- `main.py`: Este script es el punto de entrada para ejecutar el modelo. Carga los datos, inicializa el solver, construye el modelo y lo resuelve. Finalmente, imprime la solución en la consola.
- `test/`: Contiene el archivo de Excel de prueba.
- `data_test.py`: Se utiliza para generar el archivo de Excel de prueba.