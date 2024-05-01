from flask import Flask, request, jsonify
import numpy as np
import joblib  # If your model is a .pkl file
from tensorflow import keras  # If your model is a .h5 file
# import logging
import logging


app = Flask(__name__)

# Load your trained model (choose the right loading mechanism based on your model file)
# model = joblib.load('model.pkl') # For scikit-learn models
# initialize logging file
print("AAAA")
logging.basicConfig(filename='app.log', level=logging.DEBUG)

model_path = "model.h5"
model_path = "LSTM-2024_03_10-12_11_03_AM.h5"
model_path = "LSTMlast-2024_03_11-01_23_33_PM.h5"
model = keras.models.load_model(model_path)  # For Keras models


print("BBBB")


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract the object of arrays from the incoming request
        data = request.json

        data_list = data['dataList']
        # print(data)
        print("Data List")
        # print(data_list)
        # Convert arrays to a suitable numpy format for prediction
        prediction_input = [[entry['pitch'], entry['roll'],
                             entry['yaw']] for entry in data_list]

        # add 180 divide by 360 to normalize
        prediction_input = np.array(prediction_input)

        # Applying the operation to the left and right elements of each sub-array
        prediction_input[:, 0] = (prediction_input[:, 0] + 180) % 360
        prediction_input[:, -1] = (prediction_input[:, -1] + 180) % 360
        # prediction_input = prediction_input + 180
        # prediction_input = prediction_input % 360
        print(prediction_input)
        # prediction_input = prediction_input / 360
        # print(prediction_input)

# Convert to NumPy array
        arr = np.array([prediction_input])

        print("Req Received")
        # arr = np.array([[
        #     [180.5, 180, 180],
        #     [180, 180, 180],
        #     [180, 180, 180],
        #     [180, 180, 180],
        #     [180, 180, 180],
        #     [180, 180, 180],
        #     [180, 180, 180],
        #     [180, 180, 180],
        #     [180, 180, 180],
        #     [180, 180, 180],
        # ]])
        # print(arr)
        result_value = model.predict(arr)
        print(result_value)
        response = True if result_value[0][0] > 0.55 else False
        print(response)
        # log success into file
        logging.info('Prediction successful. Response: ' +
                     str(response) + ' Result: ' + str(result_value[0][0]))

        return jsonify({'is_attentive': response, 'result': str(result_value[0][0])})

    except Exception as e:
        # log error
        logging.error(str(e))
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
