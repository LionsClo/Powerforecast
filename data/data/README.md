Data sources & usage

Sources recommandées:

NASA POWER API (utilisé par data/fetch_data.py)
Kaggle, UCI, HDX, Zenodo selon besoin
Usage:

Pour générer un échantillon synthétique: python data/fetch_data.py --source synthetic --start 2020-01-01 --periods 730 --save data/sample_data.csv
Pour récupérer features météo via NASA: python data/fetch_data.py --source nasa --start 20200101 --end 20231231 --save data/sample_data.csv
Respecte les licences et anonymise toute donnée sensible avant publication.
