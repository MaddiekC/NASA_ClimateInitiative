import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# Carga del dataset
ruta_archivo = Path(__file__).parent / 'Resource' / 'pilot_topdown_CO2_Budget_countries_v1.xls'
dataset = pd.read_excel(ruta_archivo)
dataset_ref = pd.read_excel(ruta_archivo)

#print(dataset.columns)
dataset = dataset[dataset['Year'].apply(lambda x: str(x).isdigit())]
dataset_ref = dataset_ref[dataset_ref['Year'].apply(lambda x: str(x).isdigit())]

#metodo para tener informacion del pais selecionado
def obtener_informacion(pais, anio):
    # Filtrar el dataset según el país y el año
    resultado = dataset[(dataset['Alpha 3 Code'] == pais) & (dataset['Year'] == anio)]
    
    # Verificar si se encontró algún resultado
    if resultado.empty:
        return f"No se encontraron datos para el país {pais} en el año {anio}."
    
    return resultado

def calcular_emisiones(anio, pais, porcentaje_emisiones):
    # Convertir el año a entero por si viene en formato de cadena
    anio = int(anio)
    # Definición de constantes para los nombres de las columnas
    COL_ALPHA_3_CODE = 'Alpha 3 Code'
    COL_YEAR = 'Year'
    COL_FF_TGCO2 = 'FF (TgCO2)'
    COL_FF_UNC_TGCO2 = 'FF unc (TgCO2)'
  
    # Obtener los datos para el año dado
    datos_actuales = dataset[(dataset[COL_ALPHA_3_CODE] == pais) & (dataset[COL_YEAR] == anio)]

    # Verificar si se encontraron datos para el año dado
    if datos_actuales.empty:
        return f"No se encontraron datos para el país {pais} en el año {anio}."

    # Obtener las emisiones y la incertidumbre del año actual
    emisiones_actuales = float(datos_actuales[COL_FF_TGCO2].values[0])
    incertidumbre_actual = float(datos_actuales[COL_FF_UNC_TGCO2].values[0])

    # Obtener los datos para el siguiente año
    anio_siguiente = anio + 1
    datos_siguientes = dataset[(dataset[COL_ALPHA_3_CODE] == pais) & (dataset[COL_YEAR] == anio_siguiente)]

    # Verificar si se encontraron datos para el siguiente año
    if datos_siguientes.empty:
        return f"No se encontraron datos para el país {pais} en el año {anio_siguiente}."

    # Obtener las emisiones y la incertidumbre del año siguiente
    emisiones_siguientes = float(datos_siguientes[COL_FF_TGCO2].values[0])
    incertidumbre_siguientes = float(datos_siguientes[COL_FF_UNC_TGCO2].values[0])

    # Calcular el cambio porcentual de emisiones entre los años
    cambio_emisiones = ((emisiones_siguientes - emisiones_actuales) / emisiones_actuales) * 100
    
    # Calcular el cambio porcentual de incertidumbre entre los años
    cambio_incertidumbre = ((incertidumbre_siguientes - incertidumbre_actual) / incertidumbre_actual) * 100

    # Calcular el valor flotante correspondiente al porcentaje enviado por parámetro
    aumento_emisiones = (emisiones_actuales * porcentaje_emisiones) / 100
    aumento_incertidumbre = (incertidumbre_actual * porcentaje_emisiones) / 100

    # Calcular las nuevas emisiones y nuevas incertidumbres para el año actual
    nuevas_emisiones = emisiones_actuales + aumento_emisiones
    nuevas_incertidumbres = incertidumbre_actual + aumento_incertidumbre

    # Actualizar el dataset con los nuevos valores para el año actual
    dataset.loc[(dataset[COL_ALPHA_3_CODE] == pais) & (dataset[COL_YEAR] == anio), COL_FF_TGCO2] = nuevas_emisiones
    dataset.loc[(dataset[COL_ALPHA_3_CODE] == pais) & (dataset[COL_YEAR] == anio), COL_FF_UNC_TGCO2] = nuevas_incertidumbres

    # Guardar los resultados de las emisiones e incertidumbres en un diccionario
    resultados = {
        anio: {
            "emisiones": nuevas_emisiones,
            "incertidumbre": nuevas_incertidumbres
        }
    }

    # Aplicar el mismo cambio a cada año siguiente
    for i in range(len(dataset)):
        fila = dataset.iloc[i]
        # Asegurar que 'year' se compare como entero
        if fila[COL_ALPHA_3_CODE] == pais and int(fila[COL_YEAR]) > anio:
            # Sumar el aumento basado en el porcentaje a los años siguientes
            nuevas_emisiones = float(fila[COL_FF_TGCO2]) + aumento_emisiones
            nuevas_incertidumbres = float(fila[COL_FF_UNC_TGCO2]) + aumento_incertidumbre
            
            # Actualizar el dataset con los nuevos valores
            dataset.loc[(dataset[COL_ALPHA_3_CODE] == pais) & (dataset[COL_YEAR] == fila[COL_YEAR]), COL_FF_TGCO2] = nuevas_emisiones
            dataset.loc[(dataset[COL_ALPHA_3_CODE] == pais) & (dataset[COL_YEAR] == fila[COL_YEAR]), COL_FF_UNC_TGCO2] = nuevas_incertidumbres

            # Guardar los nuevos resultados
            resultados[int(fila[COL_YEAR])] = {
                "emisiones": nuevas_emisiones,
                "incertidumbre": nuevas_incertidumbres
            }

    return {
        "cambio_porcentual_emisiones": cambio_emisiones,
        "cambio_porcentual_incertidumbre": cambio_incertidumbre,
        "resultados_emisiones": resultados
    }

def graficar_emisiones(dataset_ref, dataset, pais, anio_inicial, anio_final):
    COL_ALPHA_3_CODE = 'Alpha 3 Code'
    COL_YEAR = 'Year'
    COL_FF_TGCO2 = 'FF (TgCO2)'
    COL_FF_UNC_TGCO2 = 'FF unc (TgCO2)'

    # Filtrar los datos originales del país dentro del rango de años (dataset_ref)
    datos_pais_ref = dataset_ref[(dataset_ref[COL_ALPHA_3_CODE] == pais) & 
                                 (dataset_ref[COL_YEAR] >= anio_inicial) & 
                                 (dataset_ref[COL_YEAR] <= anio_final)]

    # Filtrar los datos modificados del país dentro del rango de años (dataset)
    datos_pais_mod = dataset[(dataset[COL_ALPHA_3_CODE] == pais) & 
                             (dataset[COL_YEAR] >= anio_inicial) & 
                             (dataset[COL_YEAR] <= anio_final)]

    # Verificar si hay registros dentro del rango de años
    if datos_pais_ref.empty or datos_pais_mod.empty:
        print(f"No hay suficientes datos entre {anio_inicial} y {anio_final} para el país {pais}.")
        return
    
    # Extraer los años
    años_ref = datos_pais_ref[COL_YEAR].astype(int).values
    años_mod = datos_pais_mod[COL_YEAR].astype(int).values

    # Extraer las emisiones e incertidumbre de los datos originales (dataset_ref)
    emisiones_originales = datos_pais_ref[COL_FF_TGCO2].values
    incertidumbre_original = datos_pais_ref[COL_FF_UNC_TGCO2].values

    # Extraer las emisiones e incertidumbre de los datos modificados (dataset)
    emisiones_modificadas = datos_pais_mod[COL_FF_TGCO2].values
    incertidumbre_modificada = datos_pais_mod[COL_FF_UNC_TGCO2].values

    # Crear una figura y eje
    plt.figure(figsize=(10, 6))

    # Graficar las emisiones originales
    plt.plot(años_ref, emisiones_originales, label='Emisiones originales', color='blue', marker='o')

    # Graficar la incertidumbre original
    plt.plot(años_ref, incertidumbre_original, label='Incertidumbre original', color='green', marker='o', linestyle='--')

    # Graficar las emisiones modificadas
    plt.plot(años_mod, emisiones_modificadas, label='Emisiones modificadas', color='red', marker='o')

    # Graficar la incertidumbre modificada
    plt.plot(años_mod, incertidumbre_modificada, label='Incertidumbre modificada', color='orange', marker='o', linestyle='--')

    # Añadir títulos y etiquetas
    plt.title(f'Comparación de emisiones de cobustibles fosiles de CO2 y su incertidumbre en {pais} (años {anio_inicial} - {anio_final})')
    plt.xlabel('Año')
    plt.ylabel('Emisiones (TgCO2)')
    
    # Añadir leyenda
    plt.legend()

    # Mostrar el gráfico
    plt.grid(True)
    plt.show()

def graficar_comparacion_emisiones(dataset_ref, dataset, pais1, pais2, anio_inicial, anio_final):
    COL_ALPHA_3_CODE = 'Alpha 3 Code'
    COL_YEAR = 'Year'
    COL_FF_TGCO2 = 'FF (TgCO2)'
    COL_FF_UNC_TGCO2 = 'FF unc (TgCO2)'

    # Filtrar los datos del primer país (dataset_ref y dataset)
    datos_pais1_ref = dataset_ref[(dataset_ref[COL_ALPHA_3_CODE] == pais1) & 
                                  (dataset_ref[COL_YEAR] >= anio_inicial) & 
                                  (dataset_ref[COL_YEAR] <= anio_final)]
    
    datos_pais1_mod = dataset[(dataset[COL_ALPHA_3_CODE] == pais1) & 
                              (dataset[COL_YEAR] >= anio_inicial) & 
                              (dataset[COL_YEAR] <= anio_final)]

    # Filtrar los datos del segundo país (dataset_ref y dataset)
    datos_pais2_ref = dataset_ref[(dataset_ref[COL_ALPHA_3_CODE] == pais2) & 
                                  (dataset_ref[COL_YEAR] >= anio_inicial) & 
                                  (dataset_ref[COL_YEAR] <= anio_final)]
    
    datos_pais2_mod = dataset[(dataset[COL_ALPHA_3_CODE] == pais2) & 
                              (dataset[COL_YEAR] >= anio_inicial) & 
                              (dataset[COL_YEAR] <= anio_final)]

    # Verificar si hay suficientes registros en ambos países y años
    if datos_pais1_ref.empty or datos_pais1_mod.empty or datos_pais2_ref.empty or datos_pais2_mod.empty:
        print(f"No hay suficientes datos para los países {pais1} y {pais2} entre {anio_inicial} y {anio_final}.")
        return

    # Extraer los años
    años_pais1 = datos_pais1_ref[COL_YEAR].astype(int).values
    años_pais2 = datos_pais2_ref[COL_YEAR].astype(int).values

    # Extraer las emisiones e incertidumbre de los datos originales y modificados
    # Primer país
    emisiones_pais1_originales = datos_pais1_ref[COL_FF_TGCO2].values
    incertidumbre_pais1_original = datos_pais1_ref[COL_FF_UNC_TGCO2].values
    emisiones_pais1_modificadas = datos_pais1_mod[COL_FF_TGCO2].values
    incertidumbre_pais1_modificada = datos_pais1_mod[COL_FF_UNC_TGCO2].values

    # Segundo país
    emisiones_pais2_originales = datos_pais2_ref[COL_FF_TGCO2].values
    incertidumbre_pais2_original = datos_pais2_ref[COL_FF_UNC_TGCO2].values
    emisiones_pais2_modificadas = datos_pais2_mod[COL_FF_TGCO2].values
    incertidumbre_pais2_modificada = datos_pais2_mod[COL_FF_UNC_TGCO2].values

    # Crear una figura y eje
    plt.figure(figsize=(12, 7))

    # Graficar emisiones e incertidumbre del primer país (original y modificado)
    plt.plot(años_pais1, emisiones_pais1_originales, label=f'Emisiones originales {pais1}', color='blue', marker='o')
    plt.plot(años_pais1, incertidumbre_pais1_original, label=f'Incertidumbre original {pais1}', color='green', marker='o', linestyle='--')
    plt.plot(años_pais1, emisiones_pais1_modificadas, label=f'Emisiones modificadas {pais1}', color='red', marker='o')
    plt.plot(años_pais1, incertidumbre_pais1_modificada, label=f'Incertidumbre modificada {pais1}', color='orange', marker='o', linestyle='--')

    # Graficar emisiones e incertidumbre del segundo país (original y modificado)
    plt.plot(años_pais2, emisiones_pais2_originales, label=f'Emisiones originales {pais2}', color='purple', marker='s')
    plt.plot(años_pais2, incertidumbre_pais2_original, label=f'Incertidumbre original {pais2}', color='cyan', marker='s', linestyle='--')
    plt.plot(años_pais2, emisiones_pais2_modificadas, label=f'Emisiones modificadas {pais2}', color='magenta', marker='s')
    plt.plot(años_pais2, incertidumbre_pais2_modificada, label=f'Incertidumbre modificada {pais2}', color='yellow', marker='s', linestyle='--')

    # Añadir títulos y etiquetas
    plt.title(f'Comparación de emisiones de CO2 y su incertidumbre: {pais1} vs {pais2} ({anio_inicial}-{anio_final})')
    plt.xlabel('Año')
    plt.ylabel('Emisiones (TgCO2)')

    # Añadir leyenda
    plt.legend()

    # Mostrar el gráfico
    plt.grid(True)
    plt.show()

# Ejemplo de uso
pais_input = 'BRA'  # Reemplaza con el código del país que desees buscar
anio_input = 2017   # Reemplaza con el año que desees buscar

informacion = obtener_informacion(pais_input, anio_input)
print(informacion[['FF (TgCO2)', 'FF unc (TgCO2)']])

# Ejemplo de uso
anio_input = 2019  # Reemplaza con el año que desees buscar
pais_input = 'ECU'  # Reemplaza con el código del país que desees buscar
porcentaje_input = 20.0  # Reemplaza con el valor del porcentaje a aumentar (puede ser positivo o negativo)

resultado = calcular_emisiones(anio_input, pais_input, porcentaje_input)


# Verificar si el resultado es un mensaje de error o un diccionario con los resultados
if isinstance(resultado, str):
    print(resultado)
else:
    # print("Cambio porcentual en las emisiones:", resultado['cambio_porcentual_emisiones'])
    # print("Cambio porcentual en la incertidumbre:", resultado['cambio_porcentual_incertidumbre'])
    print("Resultados de emisiones y incertidumbre por año:")
    for anio, valores in resultado['resultados_emisiones'].items():
        print(f"Año {anio}: Emisiones = {valores['emisiones']}, Incertidumbre = {valores['incertidumbre']}")


# Ejemplo de uso
pais_input = 'ECU'  # Reemplaza con el código del país que desees buscar
anio_input = 2019   # Reemplaza con el año que desees buscar

informacion = obtener_informacion(pais_input, anio_input)
print(informacion[['FF (TgCO2)', 'FF unc (TgCO2)']])

# # Parámetros de entrada
# anio_inicial = 2010  # El año inicial del rango
# anio_final = 2019    # El año final del rango
# pais_input = 'ECU'   # El código del país que deseas graficar

# # Llamar a la función para graficar
# graficar_emisiones(dataset_ref, dataset, pais_input, anio_inicial, anio_final)

# Parámetros de entrada
anio_inicial = 2010  # Año inicial
anio_final = 2019    # Año final
pais1_input = 'ECU'  # Primer país
pais2_input = 'BRA'  # Segundo país

# Llamar a la función para graficar
graficar_comparacion_emisiones(dataset_ref, dataset, pais1_input, pais2_input, anio_inicial, anio_final)






