import joblib
import numpy as np
import pandas as pd

features = [
    "sharper",
    "volatility",
    "log_return",
    "mean_close",
    "std_close",
    "max_close",
    "min_close",
    "mean_volume",
    "std_volume",
    "mean_rsi",
    "std_rsi",
    "mean_macd",
    "std_macd",
]


def calculate_sharper(df):
    return (df["log_return"].mean() / df["log_return"].std()) * np.sqrt(
        252
    )  # Ajustado para anualización


def calculate_rsi(series, period=14):
    delta = series.diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def calculate_macd(df, slow=26, fast=12, signal=9):
    df["ema_slow"] = df["close"].ewm(span=slow, adjust=False).mean()
    df["ema_fast"] = df["close"].ewm(span=fast, adjust=False).mean()
    df["macd"] = df["ema_fast"] - df["ema_slow"]
    df["signal"] = df["macd"].ewm(span=signal, adjust=False).mean()
    return df["macd"] - df["signal"]


class ClassifierRandomCoin:
    def __init__(self):
        self.model = joblib.load("../models/random_forest.joblib")
        self.scaler = joblib.load("../models/scaler_forest.joblib")

    def __get_features(self, df: pd.DataFrame):
        features = {}
        # preprocess
        # feature engineering
        df["log_return"] = np.log(df["close"] / df["close"].shift(1))
        features["sharper"] = calculate_sharper(df)
        df["volatility"] = (df["high"] - df["low"]) / df["low"]
        features["volatility"] = df["volatility"].mean()
        features["log_return"] = df["log_return"].mean()
        features["mean_close"] = df["close"].mean()
        features["std_close"] = df["close"].std()
        features["max_close"] = df["close"].max()
        features["min_close"] = df["close"].min()
        features["mean_volume"] = df["volume"].mean()
        features["std_volume"] = df["volume"].std()
        df["rsi"] = calculate_rsi(df["close"])
        features["mean_rsi"] = df["rsi"].mean()
        features["std_rsi"] = df["rsi"].std()
        df["macd"] = calculate_macd(df)
        features["mean_macd"] = df["macd"].mean()
        features["std_macd"] = df["macd"].std()
        return pd.DataFrame(features, index=[0])

    def __prepare_input(self, data: list[dict]):
        df = pd.DataFrame(data)
        features = self.__get_features(df)
        # scale data
        return self.scaler.transform(features)

    def predict(self, data: list[dict]):
        x = self.__prepare_input(data)
        prediction = self.model.predict(x)
        print(prediction)
        return prediction[0]
