"""Authentication function."""
import urllib.parse

import requests
import streamlit as st
from ai_service_ui.settings import settings


def authenticate_page(show_button=True):
    """Display the authentication page and handle the authentication process."""
    # Step 1: Redirect to Keycloak for authentication
    if 'code' not in st.query_params:  # If the authorization code isn't in the URL
        # Generate the Keycloak authentication URL
        keycloak_auth_url = f"{settings.keycloak_base_url}/protocol/openid-connect/auth"
        params = {
            "client_id": settings.client_id,
            "redirect_uri": settings.redirect_uri,  # The URL to which Keycloak will redirect after successful login
            "response_type": "code",  # Use the authorization code flow
            "scope": "openid",  # Add any required scopes (e.g., openid, profile)
        }

        # Build the URL with parameters
        auth_url = f"{keycloak_auth_url}?{urllib.parse.urlencode(params)}"

        if show_button:  # Only show the button if called outside header
            if st.button("OTP Login"):
                st.markdown(f'<meta http-equiv="refresh" content="0; url={auth_url}">', unsafe_allow_html=True)
        else:
            st.markdown(f'<meta http-equiv="refresh" content="0; url={auth_url}">', unsafe_allow_html=True)

    # Step 2: Handle the callback after the user logs in
    else:
        # Extract the authorization code from the URL
        code = st.query_params.get('code')

        if code:
            # Exchange the authorization code for an access token
            token_url = f"{settings.keycloak_base_url}/protocol/openid-connect/token"
            token_data = {
                "client_id": settings.client_id,
                "code": code,
                "redirect_uri": settings.redirect_uri,  # The same redirect URI used in the initial request
                "grant_type": "authorization_code",
            }

            try:
                # Send the request to exchange the code for a token
                token_response = requests.post(token_url, data=token_data)
                token_response.raise_for_status()  # Raise an exception for HTTP errors

                # Check if the token exchange was successful
                if token_response.status_code == 200:
                    token_data = token_response.json()
                    access_token = token_data["access_token"]
                    id_token = token_data["id_token"]

                    # Store the access token in session state
                    st.session_state.token = f"Bearer {access_token}"
                    st.session_state.id_token = id_token

                    st.success("Authenticated successfully with Keycloak.")
                else:
                    st.error(f"Failed to exchange authorization code for tokens. Status Code: {token_response.status_code}")
                    st.error(f"Error: {token_response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error occurred during token exchange: {str(e)}")
        else:
            st.error("Authentication failed. Please try again.")
