#!/usr/bin/env python3
import argparse
from pathlib import Path
import joblib
from src.features import prepare_features
from src.model import train_xgb
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pandas as pd

def main(args):
    df, X, y = prepare_features(args.data)
    model = train_xgb(X, y)
    preds = model.predict(X)
    mae = mean_absolute_error(y, preds)
    rmse = mean_squared_error(y, preds, squared=False)
    print(f"MAE: {mae:.3f}, RMSE: {rmse:.3f}")
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model":model, "features":list(X.columns)}, args.out)
    df["pred"] = preds
    df.to_csv("models/training_diagnostics.csv", index=False)
    print("Saved model to", args.out)

if name == "main":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--out", default="models/power_model.pkl")
    args = parser.parse_args()
    main(args)
