import argparse
import json
import pickle
from logging import DEBUG

import pandas as pd
from ai_service_ui.logger import logger as logging
from flask import Flask, jsonify, request

app = Flask(__name__)
logger = logging.get_logger(__name__)
logging.get_logger().setLevel(DEBUG)


@app.before_first_request
def activate_job():
    """Activate function."""
    global metrics_json
    global model

    # Función de entrada al script de consola
    parser = argparse.ArgumentParser()

    # Parametro para el fichero de configuración del entorno
    parser.add_argument("-p", "--pkl_filename", type=str, required=True)
    parser.add_argument("-m", "--metrics_filename", type=str, required=True)

    args = parser.parse_args()

    pkl_filename = args.pkl_filename
    metrics_filename = args.metrics_filename

    metrics_json = get_model_metrics(metrics_filename)

    logger.info("Loading model ")

    # Load from file
    with open(pkl_filename, "rb") as file:
        model = pickle.load(file)

    logger.info("Models loaded")


def get_model_prediction(data: dict) -> dict:
    """Return model.

    Args:
        data (dict): data

    Returns: model

    """
    global model

    logging.debug("get_prediction(): started.")
    X = pd.DataFrame(data)

    pred = model.predict(X)

    dictionary = {"species": list(pred)}

    logger.debug("get_prediction(): final model prediction done.")

    return dictionary


def get_model_metrics(metrics_filename: json) -> dict:
    """Return metrics model.

    Args:
        metrics_filename (json): input json file

    Returns: metrics model

    """
    with open(metrics_filename) as json_file:
        data = json.load(json_file)
    return data


@app.route("/predict-values", methods=["POST"])
def predict_values():
    """Upload image with base64 format and get car make model and year response."""
    global metrics_json
    data = request.get_json()

    preds = get_model_prediction(data)

    output = dict(preds=preds, metrics=metrics_json)

    return jsonify(output)


if __name__ == "__main__":
    app.run(debug=True, threaded=False, host="0.0.0.0")
