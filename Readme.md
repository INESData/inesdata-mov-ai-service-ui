ai-service-ui
==============================

A short summary

ai service ui

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