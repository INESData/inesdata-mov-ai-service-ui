"""Header component."""
import urllib

import streamlit as st
from ai_service_ui.settings import settings
from ai_service_ui.utils.authenticate import authenticate_page


def logout():
    """Handle user logout by clearing session state and redirecting to Keycloak's logout endpoint."""
    if "token" in st.session_state:
        # Construct the logout URL
        logout_url = f"{settings.keycloak_base_url}/protocol/openid-connect/logout"
        params = {
            "client_id": settings.client_id,  # Required for public clients
            "post_logout_redirect_uri": settings.redirect_uri,  # Redirect after logout
        }

        # Build the logout URL
        full_logout_url = f"{logout_url}?{urllib.parse.urlencode(params)}"

        # Clear session state
        st.session_state.pop("token", None)
        st.session_state.pop("id_token", None)

        # Redirect user to logout URL
        st.markdown(f'<meta http-equiv="refresh" content="0; url={full_logout_url}">', unsafe_allow_html=True)

def header():
    """Render the content header in the Streamlit application."""
    # Create a login/logout button in the top-right corner
    col1, col2, col3 = st.columns([0.7, 0.2, 0.1])  # Adjust column sizes
    with col3:
        # Add custom CSS to make sure button text doesn't split
        st.markdown(
            """
            <style>
            .stButton>button {
                white-space: nowrap;
                width: 100px;  /* Adjust this value as needed */
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        if "token" in st.session_state:
            if st.button("Logout"):
                logout()
        else:
            if st.button("Login"):
                authenticate_page(show_button=False)

    # Title after the login button
    st.markdown("<h1 style='margin-top: -10px;'>InesDATA</h1>", unsafe_allow_html=True)

    st.write("""
             En esta página, exploraremos cómo los **espacios de datos** pueden facilitar el acceso y el uso eficiente de la información, y cómo estos espacios tienen un gran potencial para optimizar el **transporte público**, fomentar la **sostenibilidad** y mejorar la **calidad de vida** en nuestras ciudades. Gracias a la integración de fuentes de datos abiertos y tecnologías avanzadas de análisis, es posible gestionar el transporte público de manera más eficiente, predecir tiempos de llegada y mejorar la experiencia de los usuarios.

             A continuación, se introducirá brevemente tanto el concepto de espacio de datos como el caso de uso en cuestión. Por otro lado, en la sección  [Información de líneas y paradas](#stop-line-information) se podrá conocer toda la información de las líneas y paradas disponibles incluidas hasta el momento.

             Por último, en la sección [Predicción del tiempo de llegada](#bus-time-arrival) se podrá consultar la predicción del tiempo de llegada de un autobús a una parada y línea concreta.
            """)
