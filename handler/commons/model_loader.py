import joblib
from google.cloud.storage import Client
from keras import models


def load_model(filename: str, storage_client: Client, is_classification: bool = False):
    bucket = storage_client.bucket("garasee-ml")

    blob = bucket.blob(filename)

    local_model_filename = './tmp/' + filename
    blob.download_to_filename(local_model_filename)

    if is_classification:
        return models.load_model(local_model_filename)

    return joblib.load(local_model_filename)
