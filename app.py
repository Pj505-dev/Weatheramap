from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

DATA_URL = "https://samples.openweathermap.org/data/2.5/box/city?bbox=12,32,15,37,10&appid=b6907d289e10d714a6e88b30761fae22"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cities", methods=["POST"])
def get_cities():
    data = request.get_json()
    letter = data.get("letter", "").strip().lower()

    if not letter or len(letter) != 1:
        return jsonify({"error": "Please enter a single letter."}), 400

    try:
        response = requests.get(DATA_URL)
        response.raise_for_status()
        cities = response.json().get("list", [])

        # Filter city names starting with the given letter

        matching_cities = [city["name"] for city in cities if city["name"].lower().startswith(letter)]
        data={'cities':matching_cities,'count':len(matching_cities)}
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
