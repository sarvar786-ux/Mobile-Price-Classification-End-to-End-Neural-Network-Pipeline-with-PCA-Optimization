from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Load Model and Preprocessors
model = load_model('mobile_price_model.keras')
pca = joblib.load('pca.pkl')
scalers = joblib.load('scalers.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        # 1. Collect Input Data (20 Features)
        # Note: We must ensure the order matches the training data EXACTLY
        input_data = pd.DataFrame([{
            'battery_power': float(data['battery_power']),
            'blue': int(data['blue']),
            'clock_speed': float(data['clock_speed']),
            'dual_sim': int(data['dual_sim']),
            'fc': float(data['fc']),
            'four_g': int(data['four_g']),
            'int_memory': float(data['int_memory']),
            'm_dep': float(data['m_dep']),
            'mobile_wt': float(data['mobile_wt']),
            'n_cores': float(data['n_cores']),
            'pc': float(data['pc']),
            'px_height': float(data['px_height']),
            'px_width': float(data['px_width']),
            'ram': float(data['ram']),
            'sc_h': float(data['sc_h']),
            'sc_w': float(data['sc_w']),
            'talk_time': float(data['talk_time']),
            'three_g': int(data['three_g']),
            'touch_screen': int(data['touch_screen']),
            'wifi': int(data['wifi'])
        }])

        # 2. Apply Scaling (Same as Notebook)
        # We access the specific scalers we saved in the dictionary
        input_data['battery_power'] = scalers['battery_power'].transform(input_data[['battery_power']])
        input_data['int_memory'] = scalers['int_memory'].transform(input_data[['int_memory']])
        input_data['mobile_wt'] = scalers['mobile_wt'].transform(input_data[['mobile_wt']])
        input_data['px_height'] = scalers['px_height'].transform(input_data[['px_height']])
        input_data['px_width'] = scalers['px_width'].transform(input_data[['px_width']])
        input_data['ram'] = scalers['ram'].transform(input_data[['ram']])
        input_data['sc_h'] = scalers['sc_h'].transform(input_data[['sc_h']])
        input_data['talk_time'] = scalers['talk_time'].transform(input_data[['talk_time']])

        # 3. Apply PCA
        pca_data = pca.transform(input_data)

        # 4. Predict
        prediction = model.predict(pca_data)
        predicted_class = np.argmax(prediction, axis=1)[0]

        # Map class to Price Range
        price_map = {0: "Low Cost", 1: "Medium Cost", 2: "High Cost", 3: "Very High Cost"}
        result = price_map.get(int(predicted_class), "Unknown")

        return jsonify({'prediction': result})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)