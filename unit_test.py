import unittest
import json
from app import app  # Import your Flask app here


class PredictEndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_predict_endpoint(self):
        # Sample data payload
        data = {
            "dataList": [
                {"pitch": 10, "roll": 0, "yaw": 20},
                {"pitch": 15, "roll": 5, "yaw": 25},
                {"pitch": 15, "roll": 5, "yaw": 25},
                {"pitch": 15, "roll": 5, "yaw": 25},
                {"pitch": 15, "roll": 5, "yaw": 25},
                {"pitch": 15, "roll": 5, "yaw": 25},
                {"pitch": 15, "roll": 5, "yaw": 25},
                {"pitch": 15, "roll": 5, "yaw": 25},
                {"pitch": 15, "roll": 5, "yaw": 25},
                {"pitch": 15, "roll": 5, "yaw": 25},

                # Add more sample data as needed
            ]
        }
        response = self.app.post('/predict',
                                 data=json.dumps(data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data.decode('utf-8'))
        # Check if the response has the expected keys
        self.assertIn('is_attentive', response_data)
        # Further assertions can be added based on expected response


if __name__ == '__main__':
    unittest.main()
