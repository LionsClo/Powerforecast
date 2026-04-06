#!/usr/bin/env python3
import argparse
import pandas as pd
import requests
from pathlib import Path
import numpy as np

def fetch_nasa_power(lat, lon, start, end):
    url = ("https://power.larc.nasa.gov/api/temporal/daily/point?"
           "parameters=T2M_MAX,T2M_MIN,ALLSKY_SFC_SW_DWN,PRECTOT&format=CSV")
    url += f"&community=RE&start={start}&end={end}&longitude={lon}&latitude={lat}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    from io import StringIO
    text = r.text
    header_idx = header_skip(text)
    df = pd.read_csv(StringIO(text), skiprows=header_idx)
    return df

def header_skip(text):
    for i, line in enumerate(text.splitlines()):
        if line.startswith("YEAR"):
            return i
    return 0

def generate_synthetic(start_date, periods, freq="D", seed=42):
    rng = pd.date_range(start=start_date, periods=periods, freq=freq)
    np.random.seed(seed)
    base = 100 + 20np.sin(2np.pi * (rng.dayofyear/365.0))
    noise = np.random.normal(0, 8, size=len(rng))
    if freq == "H":
        hourly = 10np.sin(2np.pi * (rng.hour/24))
        demand = base + noise + hourly
    else:
        demand = base + noise
    df = pd.DataFrame({"date": rng, "demand_kwh": demand})
    return df

def main(args):
    out = Path(args.save)
    out.parent.mkdir(parents=True, exist_ok=True)
    if args.source == "nasa":
        lat, lon = 6.3703, 2.3912
        start = args.start
        end = args.end
        df = fetch_nasa_power(lat, lon, start, end)
        # rename & parse
        if "YYYYMMDD" in df.columns:
            df = df.rename(columns={"YYYYMMDD":"date"})
            df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
        else:
            # fallback: try year,month,day columns
            if {"YEAR","MO","DY"}.issubset(df.columns):
                df["date"] = pd.to_datetime(df["YEAR"].astype(str) + df["MO"].astype(str).str.zfill(2) + df["DY"].astype(str).str.zfill(2), format="%Y%m%d")
        # synthetic demand correlated with temp & solar
        tmax = df.get("T2M_MAX", pd.Series(25, index=df.index)).fillna(df.get("T2M_MAX").mean() if "T2M_MAX" in df else 25)
        solar = df.get("ALLSKY_SFC_SW_DWN", pd.Series(0, index=df.index)).fillna(0)
        df["demand_kwh"] = (100 + 0.3tmax + 0.05solar + np.random.normal(0,10,len(df)))
        df[["date","demand_kwh","T2M_MAX","T2M_MIN","ALLSKY_SFC_SW_DWN","PRECTOT"]].to_csv(out, index=False)
        print("Saved:", out)
    else:
        df = generate_synthetic(args.start, int(args.periods), freq=args.freq)
        df.to_csv(out, index=False)
        print("Saved synthetic:", out)

if name == "main":
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", default="data/sample_data.csv")
    parser.add_argument("--source", choices=["nasa","synthetic"], default="nasa")
    parser.add_argument("--start", default="20200101")
    parser.add_argument("--end", default="20231231")
    parser.add_argument("--periods", default=365)
    parser.add_argument("--freq", default="D")
    args = parser.parse_args()
    main(args)
