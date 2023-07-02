import streamlit as st
from model import modelo_seleccion
import matplotlib.pyplot as plt

# Función para generar la gráfica de barras
def generar_grafica(candidatos, porcentajes):
    fig, ax = plt.subplots()
    ax.bar(candidatos, porcentajes)
    ax.set_xlabel('Candidatos')
    ax.set_ylabel('Porcentaje de Concordancia')
    ax.set_title('Porcentaje de Concordancia de los Candidatos')

    # Configurar el formato del eje y para mostrar el porcentaje
    ax.yaxis.set_major_formatter('{x:.0%}')
    
    # Rotar las etiquetas del eje x para mejorar la legibilidad
    plt.xticks(rotation=45)

    # Mostrar la gráfica en Streamlit
    st.pyplot(fig)
    

def main():
    st.title("¡Contrata ahora!")
    
    st.subheader("Estás a unas preguntas de conectar con el mejor talento tech para llevar tu negocio al siguiente nivel")
    
    st.text("Responde, por favor...")
    
    # Campo de entrada para el nombre
    nombre = st.text_input("Nombre")
    
    # Campo de entrada para el correo
    contacto = st.text_input("Correo")
    
    # PREGUNTAS PARA SELECCIONAR AL CANDIDATO
    
    # Pregunta de organizar prioridades
    st.subheader("¿Cuál factor consideras es tu prioridad en el desarrollo del proyecto?")
    st.text("Ordena de primero a tercero según la relevancia que tienen los siguientes factores al momento de desarrollar tu producto.")
    
    opciones_prioridades = {
        "Presupuesto": 0,
        "Fecha límite": 0,
        "Tiempo de trabajo": 0
    }
    for opcion, valor in opciones_prioridades.items():
        opciones_prioridades[opcion] = st.slider(opcion, min_value=1, max_value=3)
        
    # Validar que no se asignen los mismos valores a opciones diferentes
    valores_asignados = list(opciones_prioridades.values())
    if len(set(valores_asignados)) != len(valores_asignados):
        st.warning("Por favor, asigna valores distintos a cada opción de prioridad.")
        return
    
    # Pregunta de perfil necesario
    st.subheader("Perfil que necesitas")
    st.text("Selecciona el perfil que consideres necesario para suplir tus necesidades.")
    opciones_perfil = ["Full-Stack", "Front-End", "Back-End", "No Code", "DevOps", "Mobile", "Data Engineer", "Business Analyst", "Data Scientist", "Machine Learning Sci/Eng", "UX/UI", "Otro"]
    perfil_necesario = st.multiselect("Selecciona el perfil que consideres necesario para suplir tus necesidades.", opciones_perfil)
    
    # Validar que se haya seleccionado al menos una opción de perfil
    if not perfil_necesario:
        st.warning("Por favor, selecciona al menos una opción de perfil.")
        return
    
    # Pregunta de nivel de inglés
    st.subheader("¿Qué nivel de inglés debería tener tu desarrollador?")
    st.text("Selecciona el nivel de inglés que requieres para el proyecto.")
    opciones_ingles = ["A1", "A2", "B1", "B2", "C1", "C2", "No aplica"]
    ingles_necesario = st.multiselect("Selecciona el nivel de inglés que requieres para el proyecto.", opciones_ingles)
    
    # Validar que se haya seleccionado al menos una opción de nivel de inglés
    if not ingles_necesario:
        st.warning("Por favor, selecciona al menos una opción de nivel de inglés.")
        return
    
    # Pregunta de tecnologías
    st.subheader("¿Hay alguna tecnología específica que debería dominar tu desarrollador?")
    st.text("Selecciona las tecnologías.")

    opciones_tec = ['Java', 'React/Node', 'React.js', 'JavaScript', 'C#', 'AWS', 'Figma', 'HTML', 'Angular', 'Node.js', 'Golang', 'TypeScript', 'PostrgreSQL', 'Vue.js', 'Laravel', 'CSS', 'MongoDB', 'Flutter', 'MySQL', 'Android', 'PHP', 'WordPress', 'Vert.x']
    tecno = st.multiselect("Selecciona las tecnologías que debería dominar tu desarrollador.", opciones_tec)
    
    # Pregunta de ingeniero graduado
    st.subheader("¿Requieres un ingeniero graduado?")
    st.text("Selecciona SI o NO")
    opciones_inge = ["SI", "NO"]
    ingeniero = st.selectbox("Selecciona una opción", opciones_inge)
    
    # Botón para enviar el formulario
    if st.button("Enviar"):
        # Validación de campos obligatorios
        if nombre and contacto and opciones_prioridades and perfil_necesario and ingles_necesario and tecno and ingeniero:
            # Llamada a la función del modelo con los datos del formulario
            resultado = modelo_seleccion(opciones_prioridades, perfil_necesario, ingles_necesario, tecno, ingeniero)
            resultado = resultado['Nombre']
            nombre_candidato_1 = resultado.values[0]  
            nombre_candidato_2 = resultado.values[1]  
            nombre_candidato_3 = resultado.values[2] 
            
            # Mostrar el resultado
            st.success("Hemos encontrado a tus candidatos ideales")
            st.header("Los candidatos son:")
            st.markdown(f"- {nombre_candidato_1}")
            st.markdown(f"- {nombre_candidato_2}")
            st.markdown(f"- {nombre_candidato_3}")
        else:
            st.warning("Por favor, completa todos los campos.")
            
            
    # Obtener los tres mejores candidatos con sus porcentajes de concordancia
    candidatos_seleccionados = modelo_seleccion(opciones_prioridades, perfil_necesario, ingles_necesario, tecno, ingeniero)
    porcentajes_concordancia = candidatos_seleccionados['Puntos'] / candidatos_seleccionados['Puntos'].sum()

    generar_grafica(candidatos_seleccionados['Nombre'], porcentajes_concordancia)


if __name__ == "__main__":
    main()