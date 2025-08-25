import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def make_features(df, horizon_days=21, lookbacks=(5, 10, 21, 63)):
    df = df.copy().sort_values("date")
    df["ret"] = np.log(df["close"]).diff()

    for lb in lookbacks:
        df[f"rv_{lb}"] = df["ret"].rolling(lb).std() * np.sqrt(252)
        df[f"mom_{lb}"] = df["close"].pct_change(lb)

    df["target_sigma"] = (
        df["ret"].shift(-1).rolling(horizon_days).std() * np.sqrt(252)
    )

    df = df.dropna().reset_index(drop=True)
    return df

def train_sigma_model(df_features, feature_cols=None, n_splits=5, random_state=7):
    if feature_cols is None:
        feature_cols = [c for c in df_features.columns if c.startswith(("rv_", "mom_"))]

    X = df_features[feature_cols].values
    y = df_features["target_sigma"].values

    tscv = TimeSeriesSplit(n_splits=n_splits)

    model = Pipeline(steps=[
        ("scaler", StandardScaler()),
        ("rf", RandomForestRegressor(
            n_estimators=400, max_depth=8, min_samples_leaf=5, random_state=random_state))
    ])

    maes = []
    for tr, te in tscv.split(X):
        model.fit(X[tr], y[tr])
        pred = model.predict(X[te])
        mae = np.mean(np.abs(pred - y[te]))
        maes.append(mae)

    model.fit(X, y)
    return model, feature_cols, float(np.mean(maes))

def predict_sigma(model, feature_cols, latest_row):
    x = latest_row[feature_cols].values.reshape(1, -1)
    sigma = float(model.predict(x)[0])
    return float(np.clip(sigma, 0.01, 3.0))
