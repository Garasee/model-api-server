from handler.commons.encoder_loader import load_encoders
from handler.commons.model_loader import load_model

CATEGORICAL_FEATURES = ['buying', 'maint', 'lug_boot', 'safety', 'class']


def acceptability_predictor_loader(storage_client):
    return {
        "model": load_model('acceptability-model.h5', storage_client, True),
        "encoders": load_encoders(storage_client, CATEGORICAL_FEATURES)
    }
