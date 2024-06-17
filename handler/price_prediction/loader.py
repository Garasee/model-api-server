from handler.commons.encoder_loader import load_encoders
from handler.commons.model_loader import load_model

CATEGORICAL_FEATURES = ['brand', 'Kondisi', 'InjeksiLangsung']


def price_predictor_loader(storage_client):
    return {
        "model": load_model('model.h5', storage_client),
        "feature_scaler": load_model('feature-scaler.h5', storage_client),
        "target_scaler": load_model('target-scaler.h5', storage_client),
        "encoders": load_encoders(storage_client, CATEGORICAL_FEATURES)
    }
