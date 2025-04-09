"""Sidebar component."""
import streamlit as st
from ai_service_ui.settings import settings


def content_sidebar():
    """Render the content sidebar in the Streamlit application."""
    with st.sidebar:
        st.image(settings.gmv_logo, width=100)
        st.sidebar.title('Tabla de contenidos')
        st.sidebar.markdown("""
                            1. [Introducción](#inesdata)

                            2. [Espacio de datos](#data-spaces)

                                2.1. [Caso de Uso: Movilidad en el Transporte Público](#use-case)

                            3. [Información de líneas y paradas](#stop-line-information)

                            4. [Predicción del tiempo de llegada](#bus-time-arrival)

                            5. [Licencia](#license)""",unsafe_allow_html=True)
