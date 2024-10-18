import pandas as pd
from services.model import ClassifierRandomCoin, ClassifierDnnCoin
from services.series import API


class CoinsRepository:
    def __init__(self):
        self.coins = pd.read_json("../datasets/json/coins_front.json")

    def get_coins_by_mark(self, n: int = 10, descending:bool = False):
        return (
            self.coins.sort_values(by="market_cap", ascending=descending)
            .head(n)
            .to_dict(orient="records")
        )

class Coins:
    def __init__(self):
        self.repository = CoinsRepository()
        self.apiService = API()
        self.modelDnn = ClassifierDnnCoin()
        self.modelRF = ClassifierRandomCoin()

    def get_coins_by_mark(self, n: int,descending:bool=False):
        return self.repository.get_coins_by_mark(n, descending)

    def get_series_by_coin(self, coin_id: str):
        return self.apiService.get_time_series(coin_id)

    def get_coins_search(self, query: str):
        return self.repository.coins[
            self.repository.coins["name"].str.contains(query, case=False)
        ].to_dict(orient="records")
    
    def predictRF(self,data:list[dict]):
        prediction = self.modelDnn.predict(data)
        metadata = self.modelRF.features(data)
        return prediction,metadata
    