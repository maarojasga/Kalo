import pandas as pd
import re

def cargar_datos():
    datos = pd.read_excel("BASE.xlsx")
    return datos

def extraer_nivel_ingles(columna):
    patron = r"A1|A2|B1|B2|C1|C2"
    columna_extraida = columna.str.extract(fr"({patron})", flags=re.IGNORECASE)[0]
    return columna_extraida

def crear_columna_graduado(datos):
    columna_titulo = datos["*Background Profesional*"]
    columna_desarrollo = datos["*Educación Formal*"]
    graduado = (columna_titulo.isin(["Pregrado", "Posgrado"])) & (columna_desarrollo.str.contains("ingenie", case=False, na=False))
    datos["Graduado"] = graduado
    return datos

def crear_columna_categoria_tiempo(datos):
    datos['Categoría Tiempo'] = datos['*Tiempo de experiencia*'].apply(lambda x: 'Presupuesto' if x in ['Sin experiencia', 'Menos de 1 año'] else 'Fecha límite' if x == 'Entre 1 a 3 años' else 'Tiempo de entrega')
    return datos

def modelo_seleccion(opciones_prioridades, perfil_necesario, ingles_necesario, tecno, ingeniero):
    datos = cargar_datos()
    datos = crear_columna_graduado(datos)
    datos = crear_columna_categoria_tiempo(datos)
    datos["Ingles"] = extraer_nivel_ingles(datos["*Nivel de Inglés*"])
    
    # Asignar puntos a los candidatos en función de sus respuestas
    datos['Puntos'] = 0
    
    # Puntos para opciones_prioridades
    for opcion, valor in opciones_prioridades.items():
        if opcion == "Presupuesto":
            datos.loc[datos['Categoría Tiempo'] == 'Presupuesto', 'Puntos'] += valor
        elif opcion == "Fecha límite":
            datos.loc[datos['Categoría Tiempo'] == 'Fecha límite', 'Puntos'] += valor
        elif opcion == "Tiempo de trabajo":
            datos.loc[datos['Categoría Tiempo'] == 'Tiempo de entrega', 'Puntos'] += valor
    
    # Puntos para perfil_necesario
    for perfil in perfil_necesario:
        datos.loc[datos['*Rol*'].str.contains(perfil, case=False), 'Puntos'] += 1
    
    # Puntos para ingles_necesario
    for nivel in ingles_necesario:
        if nivel != 'No aplica':
            datos.loc[datos['Ingles'].str.contains(nivel, case=False), 'Puntos'] += 1
    
    # Puntos para tecno
    for tecnologia in tecno:
        datos.loc[datos['*Skills*'].str.contains(tecnologia, case=False), 'Puntos'] += 1
    
    # Puntos para ingeniero
    if ingeniero == 'SI':
        datos.loc[datos['Graduado'].astype(str).str.contains('True', case=False), 'Puntos'] += 1
    
    # Obtener los tres mejores candidatos
    candidatos_seleccionados = datos.nlargest(3, 'Puntos')
    
    return candidatos_seleccionados

