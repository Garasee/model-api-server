from handler.commons.model_loader import load_model


def load_encoders(storage_client, features):
    encoder_collections = dict()
    for feature in features:
        encoder_collections[feature] = load_model(feature.lower() + '-encoders.h5', storage_client)
    return encoder_collections
