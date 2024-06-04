import joblib
from flask import Flask, request, jsonify
import pandas as pd
from google.cloud import storage

CATEGORICAL_FEATURES = ['brand', 'Kondisi', 'InjeksiLangsung']

storage_client = storage.Client.from_service_account_json('./sa.json')


def load_model(filename):
    bucket = storage_client.bucket("garasee-ml")

    blob = bucket.blob(filename)

    local_model_filename = './tmp/' + filename
    blob.download_to_filename(local_model_filename)

    model = joblib.load(local_model_filename)

    return model


def load_encoders():
    encoder_collections = dict()
    for feature in CATEGORICAL_FEATURES:
        encoder_collections[feature] = load_model(feature.lower() + '-encoders.h5')
    return encoder_collections


encoders = load_encoders()

app = Flask(__name__)

model = load_model('model.h5')
feature_scaler = load_model('feature-scaler.h5')
target_scaler = load_model('target-scaler.h5')


def handle_encoding(df, encoder):
    for feature in CATEGORICAL_FEATURES:
        if feature == "brand" and df[feature].values not in encoder[feature].classes_:
            df[feature] = "Toyota"
        df[feature] = encoder[feature].transform(df[feature])

    return df


@app.route('/predict', methods=['POST'])
def predict():
    try:
        body = request.get_json(force=True)

        data = {
            "brand": body["brand"],
            "Kondisi": "Mobil Bekas" if not body["isNew"] else "Mobil Baru",
            "TahunKendaraan": body["year"],
            "EngineCC": body["engineCapacity"],
            "TenagaPuncak(hp)": body["peakPower"],
            "TenagaPutaranPuncak(Nm)": body["peakTorque"],
            "InjeksiLangsung": body["injection"],
            "Panjang(mm)": body["length"],
            "Lebar(mm)": body["width"],
            "JarakRoda(mm)": body["wheelBase"],
        }

        df = pd.DataFrame([data])

        df_encoded = handle_encoding(df, encoders)
        df_scaled = pd.DataFrame(feature_scaler.transform(df_encoded), columns=df_encoded.columns)

        prediction = model.predict(df_scaled.values.reshape(-1, len(df_scaled.columns)))
        result = target_scaler.inverse_transform(prediction.reshape(-1, 1))[0]

        return jsonify({'price': result[0], "isAcceptable": True})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
