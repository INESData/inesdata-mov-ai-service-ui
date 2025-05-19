import json
import requests

import streamlit as st
from streamlit_modal import Modal

from components import authenticate, transfer
from settings import settings

modal = Modal(
    "Login🔒", 
    key="demo-modal",
    padding=20,    
    max_width=744  
)

def get_prediction(stop_id:str, token:str):

    if stop_id != "-":
        st.session_state["stop_id"] = stop_id                
        download_url = settings.post_api_url.format(stop_id=stop_id, line_id=st.session_state["line_id"])
    
        try:
            authorization = transfer.get_transfer(token=token, 
                                            connector_id=settings.connector_id, 
                                            contract_id=settings.contract_id_prediction, 
                                            asset_id=settings.asset_id_prediction)
            if authorization:
                headers = {
                    "X-API-Key": settings.api_key,
                    "Content-Type": "application/json",
                    "Authorization": authorization
                }
                response = requests.post(download_url, headers=headers)

                if response.status_code == 200:
                    prediction = response.json()

                    if "data" in prediction and isinstance(prediction["data"], list):
                        st.success("Predicción obtenida con éxito")

                        for item in prediction["data"]:
                            st.write(f"**Destino**: {item['destination']}")
                            if item['estimateArrive']>60:
                                st.write(f"**Tiempo estimado de llegada:** {int(round(item['estimateArrive']/60,0))} min. ")

                            else:
                                st.write(f"**Tiempo estimado de llegada:** <1 min.")

                            if item['estimateArriveAI']>60:
                                st.write(f"**Tiempo estimado (AI):** {int(round(item['estimateArriveAI']/60,0))} min.")
                            else:
                                st.write(f"**Tiempo estimado (AI):** <1 min.")     

                            st.markdown("---")  
                    else:
                        st.warning("No se encontraron datos en la respuesta.")

                elif response.status_code == 500:
                    st.error("⚠️ Hubo un problema con el servidor. Intentelo más tarde.")

                elif response.status_code == 401:
                    st.error("⚠️ La sesión ha caducado. Hacer Login de nuevo.")

                else: 
                    st.error(f"⚠️ {json.loads(response.text).get('detail', 'Error desconocido')}" )
                
        except Exception as e:
            st.error("No se pudo conectar con el servidor FastAPI.")
            st.write(e)

    else:
        st.warning("Es necesario que incluya tanto la parada como la línea para obtener la predicción.")


def bus_arrival_predictor():
    with open(settings.stop_per_lines, "r") as file:
        stop_per_lines = json.load(file)

    if st.session_state["line_id"] != "-":
        stop_id = st.selectbox(f"Seleccione la parada para la línea: {st.session_state['line_id']}",["-"] + stop_per_lines[st.session_state["line_id"]] )    
        
        # Initialize session state for button click
        if "button_clicked_prediction" not in st.session_state:
            st.session_state["button_clicked_prediction"] = False

        if st.button("Obtener predicción"): 
            st.session_state["button_clicked_prediction"] = True  # Mark that button was clicked
            if "token" not in st.session_state:
                modal.open()

        if modal.is_open():
            with modal.container():
                authenticate.authenticate_page()
                if "token" in st.session_state:
                    modal.close()

        if st.session_state["button_clicked_prediction"] and (not modal.is_open()) and ("token" in st.session_state):
            get_prediction(stop_id=stop_id, token=st.session_state["token"])