#!/usr/bin/env python3
"""
Train script variant for exploration (notebook-to-script).
Run: python notebooks/02_model_training.py --data data/sample_data.csv --out models/power_model.pkl
"""
import argparse
from src.features import prepare_features
from src.model import train_xgb
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error
from pathlib import Path

def main(data_path, out_path):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    df, X, y = prepare_features(data_path)
    model = train_xgb(X, y)
    preds = model.predict(X)
    mae = mean_absolute_error(y, preds)
    rmse = mean_squared_error(y, preds, squared=False)
    print(f"MAE: {mae:.3f}, RMSE: {rmse:.3f}")
    joblib.dump({"model":model, "features":list(X.columns)}, out_path)
    df["pred"] = preds
    df.to_csv("models/training_diagnostics.csv", index=False)
    print("Saved model and diagnostics")

if name == "main":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--out", default="models/power_model.pkl")
    args = parser.parse_args()
    main(args.data, args.out)
