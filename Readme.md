ai-service-ui
==============================

This repository contains the functions for building a User Interface that explains the INESDATA-MOV project and retrieves bus arrival time predictions. It also includes documentation on the licenses for the databases used to provide the prediction data.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## :computer: Developer guide

This section shows a way to configure a development environment.

**Requirements**:

- Python 3.11


## Prerequisites

1. Clone the repository.

    ```bash
    git clone https://dev-git.labs.gmv.com/gmv-bda/upm/inesdata-mov/ai-service-ui.git
    ```

2. Create virtual environment and activate it.

    ```bash
    python3.11 -m venv venv
    source venv/bin/activate
    ```

3. Install the requirements.

    ```bash
    pip install -r requirements/requirements.txt
    pip install -r requirements/requirements_dev.txt
    ```
3. Fill settings.py with data space components. The structure must be the following: 

    ```
    api_key: str = <THE API KEY APPEARS IN AI-SERVICE SETTINGS>

    auth_url: str = <DATA SPACE LOGIN URL>
    keycloak_base_url: str = <DATA SPACE KEYCLOACK BASE URL>

    license_api_url: str = <DATA SPACE TRANSFER ENDPOINT ASSET: LICENCIA>
    prediction_api_url: str = <DATA SPACE TRANSFER ENDPOINT ASSET: PREDICTION API>

    redirect_uri: str = "http://localhost:8501"

    start_transfer_url: str = <DATA SPACE START TRANSFER URL>
    get_transfer_url: str = <DATA SPACE GET TRANSFER URL>
    counter_party_address: str = <DATA SPACE COUNTER PARTY ADDRESS URL>
    vocabulary: str = <DATA SPACE VOCABULARY URL>

    connector_id:str = <CONNECTOR ID>
    contract_id_prediction:str = <DATA SPACE CONTRACT ID ASSET: PREDCITION API>
    asset_id_prediction:str = <DATA SPACE NAME ASSET: PREDCITION API>
    contract_id_license:str = <DATA SPACE CONTRACT ID ASSET: LICENSE>
    asset_id_license:str = <DATA SPACE NAME ASSET: LICENSE>
    client_id: str = "dataspace-users"
    grant_type: str = "password"
    ```

### Compile requirements

  We use **pip-tools** for freeze the requirements, if any package is updated the requirements need to be compiled again with pip-compile.

  ```bash
  pip-compile requirements/requirements.in
  pip-compile requirements/requirements_dev.in
  ```

### Coding style

For maintain a good `quality of code` it is **Mandatory** use pre-commit when you modify any file. This script will be launched when you try to `git commit` something, and it will display all the information. If this failed, please correct the mistake and launch again `git add` with all the files modified and `git commit` again . Please check the [detailed list of options included in pre-commit](.pre-commit-config.yaml)

### Run the app.

    ```bash
    streamlit run run.py
    ```

## Proyecto INESDATA
Este trabajo ha recibido financiación del proyecto INESData (Infraestructura para la INvestigación de ESpacios de DAtos distribuidos en UPM), un proyecto financiado en el contexto de la convocatoria UNICO I+D CLOUD del Ministerio para la Transformación Digital y de la Función Pública en el marco del PRTR financiado por Unión Europea (NextGenerationEU)