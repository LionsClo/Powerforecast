import joblib
import pandas as pd
from src.features import create_time_features, rolling_features

def load_model(path):
    obj = joblib.load(path)
    return obj["model"], obj["features"]

def prepare_input(df):
    df = df.copy()
    df = create_time_features(df)
    df = rolling_features(df)
    X = df.drop(columns=["date","demand_kwh"], errors="ignore")
    return X

def predict_from_file(model_path, input_csv):
    model, features = load_model(model_path)
    df = pd.read_csv(input_csv, parse_dates=["date"])
    X = prepare_input(df)
    X = X[features]
    preds = model.predict(X)
    return pd.DataFrame({"date":df["date"].iloc[len(df)-len(preds):],"pred":preds})
