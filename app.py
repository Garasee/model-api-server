from flask import Flask, request, jsonify
import catboost as cb
import pandas as pd

app = Flask(__name__)

# Load the CatBoost model
model = cb.CatBoostRegressor()
model.load_model('/mnt/data/catboost_tuned.h5')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON request
        data = request.get_json(force=True)
        
        # Convert JSON to DataFrame
        df = pd.DataFrame([data])
        
        # Make prediction
        prediction = model.predict(df)
        
        # Return the prediction as JSON
        return jsonify({'prediction': prediction[0]})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
