#!/usr/bin/env python3
"""
Exploration + preparation script for PowerForecast.
Run: python notebooks/01_explore_and_prep.py --data data/sample_data.csv
"""
import argparse
from src.features import load_data, create_time_features, rolling_features
import matplotlib.pyplot as plt

def main(path):
    df = load_data(path)
    print("Rows:", len(df))
    print(df.head())
    df = create_time_features(df)
    df = rolling_features(df)
    fig = plt.figure(figsize=(10,4))
    plt.plot(df['date'], df['demand_kwh'], label='demand_kwh')
    plt.title('Demand timeseries')
    plt.tight_layout()
    fig.savefig('reports/demand_timeseries.png')
    print("Saved reports/demand_timeseries.png")

if name == "main":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/sample_data.csv")
    args = parser.parse_args()
    main(args.data)
