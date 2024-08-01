import json

from microCertiSec import microCertiSec


def get_model(dfd_path: str):
    model_path = "." + dfd_path
    traceability_path = model_path.replace(".json", "_traceability.json")
    return microCertiSec.model_api(model_path, traceability_path)

def get_content(dfd_path: str) -> dict:
    with open(dfd_path, "r") as dfd_file:
        dfd = json.load(dfd_file)
    return dfd
