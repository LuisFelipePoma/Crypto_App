import pandas as pd
from services.series import API


class CoinsRepository:
    def __init__(self):
        self.coins = pd.read_json("../datasets/json/coins_front.json")

    def get_coins_bubble(self, order_by: str = "market_cap", n: int = 10):
        return (
            self.coins.sort_values(by=order_by, ascending=False)
            .head(n)
            .to_dict(orient="records")
        )


class Coins:
    def __init__(self):
        self.repository = CoinsRepository()
        self.apiService = API()

    def get_coins_list(self, n: int):
        return self.repository.get_coins_bubble(n=n)

    def get_series_by_coin(self, coin_id: str):
        return self.apiService.get_time_series(coin_id)

    def get_coins_search(self, query: str):
        return self.repository.coins[
            self.repository.coins["name"].str.contains(query, case=False)
        ].to_dict(orient="records")
