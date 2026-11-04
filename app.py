from flask import Flask, jsonify, render_template, request
from pathlib import Path

import joblib
import pandas as pd

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent 

model = joblib.load(BASE_DIR / "model.pkl") 
pipeline = joblib.load(BASE_DIR/"pipeline.pkl")

FEATURE_COLUMNS = [
    "longitude",
    "latitude",
    "housing_median_age",
    "total_rooms",
    "total_bedrooms",
    "population",
    "households",
    "median_income",
    "ocean_proximity",
]

@app.post("/api/predict")
def predict():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error":"No data recived"}),400

    missing_fields = [
        field for field in FEATURE_COLUMNS
        if field not in data
    ]
    if missing_fields :
        return jsonify({
            "error" : f"Missing  fields {', '.join(missing_fields)}"
        }),400
    
    try:
        row = {
            "longitude": float(data["longitude"]),
            "latitude": float(data["latitude"]),
            "housing_median_age": float(data["housing_median_age"]),
            "total_rooms": float(data["total_rooms"]),
            "total_bedrooms": float(data["total_bedrooms"]),
            "population": float(data["population"]),
            "households": float(data["households"]),
            "median_income": float(data["median_income"]),
            "ocean_proximity": str(data["ocean_proximity"]),
        }

        input_frame = pd.DataFrame([row], columns=FEATURE_COLUMNS)

        prepared_input = pipeline.transform(input_frame)
        prediction = float(model.predict(prepared_input)[0])

    except (TypeError, ValueError):
        return jsonify({
            "error": "One or more values are invalid."
        }), 400

    return jsonify({
        "prediction": round(prediction, 2)
    })

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)