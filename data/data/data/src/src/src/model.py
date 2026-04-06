import joblib
from xgboost import XGBRegressor
from sklearn.model_selection import TimeSeriesSplit, RandomizedSearchCV

def train_xgb(X, y):
    tscv = TimeSeriesSplit(n_splits=5)
    model = XGBRegressor(objective="reg:squarederror", n_jobs=4, random_state=42)
    param_dist = {
        "n_estimators":[100,200,400],
        "max_depth":[3,5,7],
        "learning_rate":[0.01,0.05,0.1],
        "subsample":[0.6,0.8,1.0]
    }
    search = RandomizedSearchCV(model, param_dist, cv=tscv, n_iter=10, scoring="neg_mean_absolute_error", n_jobs=1, random_state=42)
    search.fit(X, y)
    best = search.best_estimator_
    return best

def predict(model, X):
    return model.predict(X)
