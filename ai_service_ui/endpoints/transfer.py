"""Auxiliar function for data spaces transference."""
import json
import time

import requests
import streamlit as st
from ai_service_ui.settings import settings


def get_transfer(token:str, connector_id:str, contract_id:str, asset_id:str)->str:
    """Get transference.

    Args:
        token (str): Token
        connector_id (str): Connector id
        contract_id (str): Contract id
        asset_id (str): Asset id

    Returns:
        str: Athentication
    """
    try:
        start_transfer_url = settings.start_transfer_url
        start_transfer_headers = {
            "Content-Type": "application/json",
            "Authorization": token
        }
        start_transfer_data = {
        "@context": {
        "@vocab": settings.vocabulary},
        "@type": "TransferRequestDto",
        "connectorId": connector_id,
        "counterPartyAddress": settings.counter_party_address,
        "contractId": contract_id,
        "assetId": asset_id,
        "protocol": "dataspace-protocol-http",
        "transferType": "HttpData-PULL"
        }

        start_transfer_response = requests.post(start_transfer_url, json=start_transfer_data, headers=start_transfer_headers)
        start_transfer = start_transfer_response.json()

        if start_transfer_response.status_code == 200:

            transfer_id = start_transfer["@id"]

            time.sleep(7)

            get_transfer_url = settings.get_transfer_url.format(transfer_id=transfer_id)
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
