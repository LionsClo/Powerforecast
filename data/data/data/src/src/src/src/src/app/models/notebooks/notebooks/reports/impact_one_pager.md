PowerForecast — One-page impact summary
Objectif
Fournir des prévisions court terme probabilistes de la demande électrique urbaine (Cotonou) pour optimiser la dispatch, la gestion de microgrids et les réponses côté demande.

Modèle
XGBoost time-series regressor avec features temporelles et météo (données NASA POWER). Déploiement léger via Streamlit.

Impact estimé 

Demande moyenne journalière (ex.): 120 kWh
Amélioration conservative via dispatch piloté par forecast: 3–8%
Économie estimée par jour: 6 kWh (5% de 120)
Économie annuelle par node: ~2,190 kWh
CO2 évité = kWh_sauvés * facteur_émission (ex. 0.5 kgCO2/kWh)
Déploiement  

Dashboard Streamlit pour opérateurs
Entrainement périodique et pipeline CI
Intégration future avec optimisation stockage/demand response
Limitations & prochaines étapes  

Validation opérationnelle requiert données de consommation réelles
Intégrer forecasting probabiliste (quantiles / Prophet)
Couplage avec optimiseur dispatch (OPF) et stockage
