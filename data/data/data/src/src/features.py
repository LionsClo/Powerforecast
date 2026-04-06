import pandas as pd

def load_data(path):
    df = pd.read_csv(path, parse_dates=["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df

def create_time_features(df, date_col="date"):
    df["dayofyear"] = df[date_col].dt.dayofyear
    df["month"] = df[date_col].dt.month
    df["weekday"] = df[date_col].dt.weekday
    df["is_weekend"] = (df["weekday"] >= 5).astype(int)
    return df

def rolling_features(df, col="demand_kwh"):
    df[f"{col}_lag7"] = df[col].shift(7)
    df[f"{col}_lag14"] = df[col].shift(14)
    df[f"{col}_rolling7"] = df[col].rolling(7, min_periods=1).mean()
    return df

def prepare_features(path):
    df = load_data(path)
    df = create_time_features(df)
    df = rolling_features(df)
    df = df.dropna().reset_index(drop=True)
    X = df.drop(columns=["date","demand_kwh"])
    y = df["demand_kwh"]
    return df, X, y
