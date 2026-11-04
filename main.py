import os
import joblib

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV    
from sklearn.ensemble import HistGradientBoostingRegressor, ExtraTreesRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import cross_val_score

MODEL_FILE = "model.pkl"
PIPELINE_FILE = "pipeline.pkl"

def build_pipeline(num_attrib,cat_attrib):
    num_pipeline = Pipeline(
        [("impute", SimpleImputer(strategy="median")), 
        ("scaler", StandardScaler())
        ]
    )

    # creating Categorical pipelines

    cat_pipeline = Pipeline([("encoder", OneHotEncoder(handle_unknown="ignore"))])

    # full pipeline

    full_pipeline = ColumnTransformer(
        [("num", num_pipeline, num_attrib), ("cat", cat_pipeline, cat_attrib)]
    )

    return full_pipeline

if not os.path.exists(MODEL_FILE):
    # lets train the model
    housing = pd.read_csv("housing.csv")

    housing["income_cat"] = pd.cut(
        housing["median_income"],
        bins=[0, 1.5, 3.0, 4.5, 6.0, np.inf],
        labels=[1, 2, 3, 4, 5],
    )

# 2. creating a stratified splitting data for training and test

    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

    for train_index, test_index in split.split(housing, housing["income_cat"]):
        test_rows = housing.loc[test_index]
        test_rows.drop("income_cat", axis=1).to_csv("input_with_label.csv", index=False)
        test_rows.drop(["income_cat", "median_house_value"], axis=1).to_csv("input_no_label.csv", index=False)
        housing = housing.loc[train_index].drop("income_cat", axis=1)

    # 3. separate  features and labels
    housing_labels = housing["median_house_value"].copy()
    housing_features = housing.drop("median_house_value", axis=1)

    # 4. Separate numerical and catogorical columms

    num_attrib = housing_features.drop("ocean_proximity", axis=1).columns.tolist()
    cat_attrib = ["ocean_proximity"]

    pipeline = build_pipeline(num_attrib,cat_attrib)
    housing_prepared = pipeline.fit_transform(housing_features)

    model = RandomForestRegressor(
    n_estimators=300,
    max_features=6,
    min_samples_leaf=2,
    min_samples_split=5,
    bootstrap=False,
    random_state=42,
    n_jobs=-1,
)
    model.fit(housing_prepared,housing_labels)

    # saving the model

    joblib.dump(model,MODEL_FILE)
    joblib.dump(pipeline,PIPELINE_FILE)

    print(
        "Model trained and saved.\n"
        "Two test files were created:\n"
        "  - input_no_label.csv   (no prices, used for predictions)\n"
        "  - input_with_label.csv (with real prices, shown beside the predictions)\n"
        "Run this script again to get output.csv."
    )
else:
    # inference
    model = joblib.load(MODEL_FILE)
    pipeline = joblib.load(PIPELINE_FILE)

    input_data = pd.read_csv("input_no_label.csv")
    actual = pd.read_csv("input_with_label.csv")["median_house_value"]

    predictions = model.predict(pipeline.transform(input_data))

    input_data["Predicted_mh_val"] = predictions
    input_data["median_house_value"] = actual   # real price, right beside the prediction

    input_data.to_csv("output.csv", index=False)

  
    print("Result saved to output.csv")