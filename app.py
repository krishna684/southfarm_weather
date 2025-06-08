import requests
import os
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_TOKEN = os.getenv('ZENTRA_API_TOKEN')
DEVICE_ID = os.getenv('ZENTRA_DEVICE_ID')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-data')
def get_data():
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    url = f"https://api.zentracloud.com/v1/devices/{DEVICE_ID}/data"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Failed to fetch data'}), 500

if __name__ == '__main__':
    app.run(debug=True)
