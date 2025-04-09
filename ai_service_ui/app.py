import streamlit as st
from ai_service_ui.components import header, sidebar
from ai_service_ui.endpoints import get_license, get_prediction
from ai_service_ui.pages import bus_information, data_space
from ai_service_ui.settings import settings

st.set_page_config(page_title='INESDATA-MOV', layout="wide", initial_sidebar_state="auto", menu_items=None)

def create_app():
    # Load custom CSS
    with open(settings.styles) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    header.header()
    sidebar.content_sidebar()

    # Display data space section
    data_space.introduction()
    data_space.use_case()

    # Display information section
    bus_information.introduction()
    bus_information.stop_map_section()

    # Display prediction section
    get_prediction.bus_arrival_predictor()

    # Display license section
    get_license.inesdata_license()
