import joblib
import numpy as np
import pandas as pd
from datetime import datetime
from tensorflow.keras.models import load_model # type: ignore

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

def calculate_sharper(df, risk_free_rate=0):
    log_returns = np.log(df["close"] / df["close"].shift(1))
    avg_return = log_returns.mean()
    std_dev = log_returns.std()
    
    sharper_ratio = (avg_return - risk_free_rate) / std_dev
    return sharper_ratio

def calculate_rsi(series, period=14):
    delta = series.diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


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
    
    def features(self, data: list[dict]):
        x = pd.DataFrame(data)
        features = self.__get_features(x)
        return features.to_dict(orient="records")[0]


# --------------------------------------------------------------

def calculate_levelup(v1: float, v2: float) -> float:
    if v1 == 0 or v2 == 0:
        return 0.0
    return float((v2 - v1) / v1)

def get_datetime(date: str) -> datetime:
    return datetime.strptime(date, "%d/%m/%Y")

def get_data_dates(group: pd.DataFrame, MD: int, ED: int):
    start_date = group.index.min()
    start = group.loc[[start_date]].close.values[0]
    middle = group.iloc[[MD]].close.values[0]
    end =group.iloc[[ED]].close.values[0]
    return (
        start,
        middle,
        end,
    )
    
def create_data(group:pd.DataFrame, MD: int, ED: int) -> dict:
    h_start, h_md, h_ed = get_data_dates(group, MD, ED)
    new_halving = {
        "h_start": h_start,
        f"h_{MD}d": h_md,
        f"h_{ED}d": h_ed,
        f"h_{MD}d_change": calculate_levelup(h_start, h_md),
        f"h_{ED}d_change": calculate_levelup(h_start, h_ed),
        "h_max": group.close.max(),
    }
    return new_halving
    
class ClassifierDnnCoin:
    def __init__(self):
        # self.scaler = ...
        self.model = load_model("../models/best_model2.keras")
 
    def __get_features(self,df:pd.DataFrame):
        size_series = df.shape[0]
        print(size_series)
        # variables dynamic
        MD = int(size_series * 0.3)
        ED = int(size_series * 0.6)
        h = create_data(df,MD, ED)
        features = {
            "h_start": h["h_start"],
            f"h_{MD}d": h[f"h_{MD}d"],
            f"h_{MD}d_change": h[f"h_{MD}d_change"],
            f"h_{ED}d": h[f"h_{ED}d"],
            f"h_{ED}d_change": h[f"h_{ED}d_change"],
            "h_max": h["h_max"],
        }
        
        return pd.DataFrame([features])
        
        
    
    def predict(self, data:list[dict]):
        
        df = pd.DataFrame(data)
        # col "timestamp" to datetime
        df["timestamp"] = df["timestamp"].apply(lambda x: datetime.fromtimestamp(x))
        df.set_index("timestamp", inplace=True)
        features = self.__get_features(df)
        # predict
        prediction = self.model.predict(features)
        print(prediction)
        return 1 if prediction[0][0] > 0.5 else 0