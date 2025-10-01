"""
ML Volatility Helper

Description: Simple helpers to learn an annualized volatility (sigma)
from historical prices using basic rolling features and a small model.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit, cross_val_score

TRADING_DAYS = 252

def rsi(px, period=14):
    delta = px.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    roll_up = up.rolling(period).mean()
    roll_down = down.rolling(period).mean()
    rs = roll_up / (roll_down + 1e-12)
    return 100 - (100 / (1 + rs))

def ewma_vol(logret, lam=0.94, window=60):
    # RiskMetrics-style EWMA variance with finite window, then annualize
    r2 = logret.pow(2).fillna(0.0)
    w = (1 - lam) * lam ** np.arange(window)
    w = w[::-1] / w.sum()
    ewma_var = r2.rolling(window=window).apply(lambda x: np.dot(x, w), raw=True)
    return np.sqrt(ewma_var * TRADING_DAYS)

def realized_vol_next_h(logret, horizon_days):
    # std of next H returns, aligned to the start, then annualized
    fwd_std = logret.rolling(horizon_days).std().shift(-horizon_days)
    return fwd_std * np.sqrt(TRADING_DAYS)

def build_features(px):
    logret = np.log(px / px.shift(1))
    feats = pd.DataFrame(index=px.index)

    # rolling vols (annualized)
    for w in [5, 10, 20, 60]:
        feats[f"rv_{w}"] = logret.rolling(w).std() * np.sqrt(TRADING_DAYS)

    # EWMA vol
    feats["ewma_60"] = ewma_vol(logret, lam=0.94, window=60)

    # magnitude of recent returns
    for w in [5, 10, 20]:
        feats[f"mean_abs_ret_{w}"] = logret.abs().rolling(w).mean() * np.sqrt(TRADING_DAYS)

    # momentum / trend
    feats["mom_10"] = (px / px.shift(10)) - 1.0
    feats["mom_20"] = (px / px.shift(20)) - 1.0
    feats["rsi_14"] = rsi(px, 14)

    return feats, logret

def learn_sigma(
    px,
    horizon_days,
    model_type="ridge",
    min_history_days=750,
    ridge_alpha=10.0,
    rf_n_estimators=300,
    rf_max_depth=None,
    cv_splits=5
):
    """
    Returns a dict with:
      - sigma (annualized prediction for next H days)
      - mae_cv (time-series CV MAE in sigma units) or None
      - model (fitted model)
      - X_tail, y_tail (for optional quick plots/tables)
    """
    if len(px) < min_history_days:
        raise ValueError(f"Need at least {min_history_days} days of data; got {len(px)}.")

    feats, logret = build_features(px)
    y = realized_vol_next_h(logret, horizon_days)

    data = pd.concat([feats, y.rename("y")], axis=1).dropna()
    X = data.drop(columns=["y"])
    y = data["y"]

    if model_type.lower().startswith("ridge"):
        model = Ridge(alpha=float(ridge_alpha))
    else:
        model = RandomForestRegressor(
            n_estimators=int(rf_n_estimators),
            max_depth=rf_max_depth,
            random_state=42,
            n_jobs=-1
        )

    mae_cv = None
    if len(X) > (cv_splits + 30):
        tscv = TimeSeriesSplit(n_splits=cv_splits)
        scores = cross_val_score(model, X, y, cv=tscv, scoring="neg_mean_absolute_error")
        mae_cv = float(-scores.mean())

    model.fit(X, y)
    sigma_pred = float(model.predict(X.tail(1))[0])

    return {
        "sigma": sigma_pred,
        "mae_cv": mae_cv,
        "model": model,
        "X_tail": X.tail(200),
        "y_tail": y.tail(200),
    }
