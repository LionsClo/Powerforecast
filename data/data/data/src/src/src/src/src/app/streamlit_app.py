import streamlit as st
import pandas as pd
import altair as alt
from src.predict import predict_from_file
from pathlib import Path
import joblib

st.set_page_config(page_title="PowerForecast — Cotonou", layout="wide")
st.sidebar.title("PowerForecast")
st.sidebar.markdown("Forecast urban electricity demand — demo")

DATA_PATH_DEFAULT = "data/sample_data.csv"
MODEL_PATH_DEFAULT = "models/power_model.pkl"

uploaded = st.sidebar.file_uploader("Upload CSV (date,demand_kwh,optional features)", type=["csv"])
if uploaded is not None:
    df = pd.read_csv(uploaded, parse_dates=["date"])
else:
    df = pd.read_csv(DATA_PATH_DEFAULT, parse_dates=["date"])

st.sidebar.markdown("### Controls")
horizon = st.sidebar.slider("Forecast horizon (days)", 1, 30, 7)

st.title("PowerForecast — Cotonou (Demo)")
col1, col2 = st.columns([2,1])

with col1:
    st.subheader("Historical demand")
    chart = alt.Chart(df).mark_line().encode(x="date:T", y="demand_kwh:Q")
    st.altair_chart(chart, use_container_width=True)

with col2:
    st.subheader("Quick model info")
    if Path(MODEL_PATH_DEFAULT).exists():
        mdl = joblib.load(MODEL_PATH_DEFAULT)
        st.write("Model: XGBoost regressor")
        try:
            diag = pd.read_csv('models/training_diagnostics.csv', parse_dates=["date"])
            st.write(f"Training rows: {len(diag)}")
        except Exception:
            st.write("Diagnostics not available.")
    else:
        st.write("Model not trained yet. Use CLI train script.")

if st.button("Run forecast"):
    df_in = df.copy()
    last_date = df_in["date"].max()
    future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=horizon)
    future_df = pd.DataFrame({"date": future_dates})
    df_concat = pd.concat([df_in, future_df], ignore_index=True, sort=False)
    tmp = "data/_tmp_forecast_input.csv"
    df_concat.to_csv(tmp, index=False)
    results = predict_from_file(MODEL_PATH_DEFAULT, tmp)
    results["pred_lower"] = results["pred"] - 1.96 * results["pred"].std()*0.5
    results["pred_upper"] = results["pred"] + 1.96 * results["pred"].std()*0.5
    st.subheader("Forecast")
    fc_chart = alt.Chart(results).mark_line(color="red").encode(x="date:T", y="pred:Q")
    st.altair_chart(fc_chart, use_container_width=True)
    st.write(results)

st.markdown("---")
st.markdown("Diagnostics & Impact")
if Path("models/training_diagnostics.csv").exists():
    diag = pd.read_csv("models/training_diagnostics.csv", parse_dates=["date"])
    st.line_chart(diag.set_index("date")[["demand_kwh","pred"]])
    mean_forecast = diag["pred"].mean()
    potential_saving_pct = 0.05
    est_saving_kwh_per_day = mean_forecast * potential_saving_pct
    st.metric("Estimated saving per day (kWh)", f"{est_saving_kwh_per_day:.1f}")
else:
    st.write("No diagnostics available. Train model to generate impact estimates.")
