# California House Price Predictor

A Flask web application that predicts median house values in California using a Random Forest machine learning model.

## Features

- Multi-step house price prediction form
- Responsive frontend built with HTML, CSS, and JavaScript
- Flask backend API
- Random Forest regression model
- Input validation for prediction data
- California Housing dataset support

## Tech Stack

- Python
- Flask
- Pandas
- Scikit-learn
- Joblib
- HTML, CSS, JavaScript

## Project Structure

```text
project-california/
├── static/
│   ├── app.js
│   └── styles.css
├── templates/
│   └── index.html
├── app.py
├── main.py
├── housing.csv
├── model.pkl
├── pipeline.pkl
├── requirements.txt
└── README.md
```

## Model Inputs

The model uses these district features:

- Longitude
- Latitude
- Housing median age
- Total rooms
- Total bedrooms
- Population
- Households
- Median income
- Ocean proximity

## Installation

Clone the repository:

```bash
git clone https://github.com/priyajit-dev/california-house-price-predictor.git
cd california-house-price-predictor
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

If Git LFS is required for the trained model files:

```bash
git lfs install
git lfs pull
```

## Run the Application

Start the Flask server:

```bash
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

## Train the Model

If `model.pkl` and `pipeline.pkl` are missing, train the model with:

```bash
python main.py
```

## Disclaimer

This project uses the California Housing dataset. Predictions are estimates based on historical California census district data and are not real property valuations.

## License

This project is licensed under the MIT License.
