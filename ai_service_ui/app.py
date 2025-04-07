import streamlit as st

from components import header,sidebar,data_space, bus_information, service, license


st.set_page_config(page_title='INESDATA-MOV', page_icon='./assets/favicon.ico', layout="wide", initial_sidebar_state="auto", menu_items=None)

def main():
    # Load custom CSS
    with open('./ai_service_ui/public/style.css') as f:
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
    service.bus_arrival_predictor()
    
    # Display license section
    license.inesdata_license()


if __name__ == "__main__":
    main()
