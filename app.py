import os
from datetime import datetime, timedelta

import requests
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='.')

API_TOKEN = os.environ.get('ZENTRA_API_TOKEN')
DEVICE_ID = os.environ.get('ZENTRA_DEVICE_ID')


def fetch_sensor_data(device_id=DEVICE_ID, token=API_TOKEN, hours=24):
    """Fetch sensor data from ZENTRA Cloud.

    If the API cannot be reached or credentials are missing, sample data
    is generated for demonstration purposes.
    """
    start_time = datetime.utcnow() - timedelta(hours=hours)

    if not device_id or not token or token.startswith('your_actual'):
        # Return mock data when credentials are not configured
        now = datetime.utcnow()
        return [
            {
                "timestamp": (now - timedelta(hours=i)).isoformat() + "Z",
                "value": 20 + i * 0.5,
            }
            for i in reversed(range(hours))
        ]

    url = f"https://api.zentracloud.com/v3/devices/{device_id}/measurements"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"start": start_time.isoformat() + "Z"}
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data.get("measurements", [])
    except Exception as exc:
        print(f"Error fetching data from ZENTRA Cloud: {exc}")
        return []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/data")
def api_data():
    hours = int(request.args.get("hours", 24))
    data = fetch_sensor_data(hours=hours)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
