from flask import Flask, request, jsonify
from google.cloud import storage

from handler.acceptability_prediction.loader import acceptability_predictor_loader
from handler.acceptability_prediction.predictor import predict_acceptability
from handler.price_prediction.loader import price_predictor_loader
from handler.price_prediction.predictor import predict_price

app = Flask(__name__)
storage_client = storage.Client.from_service_account_json('./sa.json')

price_predictor = price_predictor_loader(storage_client)
acceptability_predictor = acceptability_predictor_loader(storage_client)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        body = request.get_json(force=True)

        price = predict_price(body, **price_predictor)

        acceptability = predict_acceptability(body, price, **acceptability_predictor)

        return jsonify({'price': price, "isAcceptable": acceptability})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
