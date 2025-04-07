import streamlit as st

def content_sidebar():
    with st.sidebar:
        st.image('./ai_service_ui/assets/gmv_logo.svg', width=100)
        st.sidebar.title('Tabla de contenidos')
        st.sidebar.markdown("""
                            1. [Introducción](#inesdata)

                            2. [Espacio de datos](#data-spaces)
                        
                                2.1. [Caso de Uso: Movilidad en el Transporte Público](#use-case)
                            
                            3. [Información de líneas y paradas](#stop-line-information)
                                                        
                            4. [Predicción del tiempo de llegada](#bus-time-arrival)
                            
                            5. [Licencia](#license)""",unsafe_allow_html=True)