import pandas as pd

from handler.commons.encoding_handler import handle_encoding
from handler.price_prediction.loader import CATEGORICAL_FEATURES


def predict_price(payload, model, feature_scaler, target_scaler, encoders):
    data = {
        "brand": "Toyota" if payload["brand"] not in encoders["brand"].classes_ else payload["brand"],
        "Kondisi": "Mobil Bekas" if not payload["isNew"] else "Mobil Baru",
        "TahunKendaraan": payload["year"],
        "EngineCC": payload["engineCapacity"],
        "TenagaPuncak(hp)": payload["peakPower"],
        "TenagaPutaranPuncak(Nm)": payload["peakTorque"],
        "InjeksiLangsung": payload["injection"],
        "Panjang(mm)": payload["length"],
        "Lebar(mm)": payload["width"],
        "JarakRoda(mm)": payload["wheelBase"],
    }

    df = pd.DataFrame([data])

    df_encoded = handle_encoding(df, encoders, CATEGORICAL_FEATURES)
    df_scaled = pd.DataFrame(feature_scaler.transform(df_encoded), columns=df_encoded.columns)

    prediction = model.predict(df_scaled.values.reshape(-1, len(df_scaled.columns)))
    result = target_scaler.inverse_transform(prediction.reshape(-1, 1))[0]

    return result[0]