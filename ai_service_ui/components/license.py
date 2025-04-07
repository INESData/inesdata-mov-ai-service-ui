import streamlit as st
import json
import requests
from settings import settings
from components import authenticate, transfer
from streamlit_modal import Modal

modal = Modal(
    "Login🔒", 
    key="demo-modal",
    padding=20,    
    max_width=744  
)

def get_license(token:str):

    try:
        authorization = transfer.get_transfer(token=token, 
                                          connector_id=settings.connector_id, 
                                          contract_id=settings.contract_id_license, 
                                          asset_id=settings.asset_id_license)
        if authorization: 
            headers = {
                "X-API-Key": settings.api_key,
                "Content-Type": "application/json",
                "Authorization": authorization
            }
            response = requests.get(settings.get_api_url, headers=headers)
            
            if response.status_code == 200:
                license_data = response.json()  # Parsear la respuesta como JSON
                if "emt" in license_data:
                    st.markdown(f"+ [EMT]({license_data['emt']})")
                if "aemet" in license_data:
                    st.markdown(f"+ [AEMET]({license_data['aemet']})")
                if "informo" in license_data:
                    st.markdown(f"+ [INFORMO]({license_data['informo']})")

            elif response.status_code == 500:
                st.error("⚠️ Hubo un problema con el servidor. Intentelo más tarde.")

            elif response.status_code == 401:
                st.error("⚠️ La sesión ha caducado. Hacer Login de nuevo.")

            else: 
                st.error(f"⚠️ {json.loads(response.text).get('detail', 'Error desconocido')}" )

    except Exception as e:
        st.error("No se pudo conectar con el servidor FastAPI.")
        st.write(e)

def inesdata_license():

    st.header("Licencia", anchor='license', divider='gray')
    st.write("En esta sección, encontrarás enlaces a las licencias de las fuentes de datos utilizadas, garantizando transparencia y cumplimiento con los términos de uso establecidos por cada proveedor.")

    # Initialize session state for button click
    if "button_clicked_license" not in st.session_state:
        st.session_state["button_clicked_license"] = False

    if st.button("Obtener licencias"): 
        st.session_state["button_clicked_license"] = True  # Mark that button was clicked
        if "token" not in st.session_state:
            modal.open()

    if modal.is_open():
        with modal.container():
            authenticate.authenticate_page()
            if "token" in st.session_state:
                modal.close()

    # Only call get_license if the button was clicked and authentication was successful
    if st.session_state["button_clicked_license"] and (not modal.is_open()) and ("token" in st.session_state):
        get_license(token=st.session_state["token"])