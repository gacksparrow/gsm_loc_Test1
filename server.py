from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Your Google Geolocation API Key
GOOGLE_API_KEY = "AIzaSyCOswgZfQzUK5o8xeW16zJInpXHMh4s7LU"

@app.route("/get_location", methods=["POST"])
def get_location():
    data = request.json
    payload = {
        "cellTowers": [{
            "cellId": data["cellId"],
            "locationAreaCode": data["lac"],
            "mobileCountryCode": data["mcc"],
            "mobileNetworkCode": data["mnc"]
        }]
    }

    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={GOOGLE_API_KEY}"
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        loc = response.json()["location"]
        maps_link = f"https://www.google.com/maps?q={loc['lat']},{loc['lng']}"
        return jsonify({
            "lat": loc["lat"],
            "lng": loc["lng"],
            "accuracy": response.json().get("accuracy", "N/A"),
            "maps_url": maps_link
        })
    else:
        return jsonify({"error": "Geolocation failed"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

