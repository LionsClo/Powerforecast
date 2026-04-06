# Powerforecast
 PowerForecast — Probabilistic urban electricity demand forecasting (Cotonou). Time‑series ML + Streamlit demo + policy brief.
 
Principaux livrables

Notebook d'exploration et d'entraînement
Modèle entraîné (joblib)
Démo interactive Streamlit
One-page impact (reports/impact_one_pager.md)
Quick start

git clone https://github.com//powerforecast.git
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python data/fetch_data.py --source synthetic --start 2020-01-01 --periods 730 --save data/sample_data.csv
python src/train.py --data data/sample_data.csv --out models/power_model.pkl
streamlit run app/streamlit_app.py
Structure du repo

data/: scripts et échantillons
src/: code pipeline (features, model, train, predict)
app/: Streamlit demo
notebooks/: scripts d'exploration et entraînement
models/: modèles sérialisés et diagnostics
reports/: one-pager impact
Licence
MIT

Notes

Utilise NASA POWER pour features météo (script data/fetch_data.py) ou fallback synthétique.
Vérifie licences données avant publication.
