import time
import json
import requests
import streamlit as st

def get_transfer(token:str, connector_id:str, contract_id:str, asset_id:str):

    try: 
        start_transfer_url = "https://conn-ses-mobility.ds.inesdata-project.eu/management/v3/transferprocesses"
        start_transfer_headers = {
            "Content-Type": "application/json",
            "Authorization": token
        }
        start_transfer_data = {
        "@context": {
        "@vocab": "https://w3id.org/edc/v0.0.1/ns/"},
        "@type": "TransferRequestDto",
        "connectorId": connector_id,
        "counterPartyAddress": "https://conn-gmv-mobility.ds.inesdata-project.eu/protocol",
        "contractId": contract_id,
        "assetId": asset_id,
        "protocol": "dataspace-protocol-http",
        "transferType": "HttpData-PULL"
        }

        start_transfer_response = requests.post(start_transfer_url, json=start_transfer_data, headers=start_transfer_headers)
        start_transfer = start_transfer_response.json()

        if start_transfer_response.status_code == 200:

            transfer_id = start_transfer["@id"]

            time.sleep(4)

            get_transfer_url = f"https://conn-ses-mobility.ds.inesdata-project.eu/management/v1/edrs/{transfer_id}/dataaddress"
            headers = {
                "Authorization": token
            }
            get_transfer_response = requests.get(get_transfer_url, headers=headers)

            get_transfer = get_transfer_response.json()
            authenticate = get_transfer["authorization"]
            return authenticate
        
        elif start_transfer_response.status_code == 401:
            st.error("⚠️ La sesión ha caducado. Hacer Login de nuevo.")
        else: 
            st.error(f"⚠️ {json.loads(start_transfer_response.text).get('detail', 'Error desconocido')}" )
        
    except Exception as e:
        st.error("")
        st.write(e)