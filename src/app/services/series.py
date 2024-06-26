from datetime import datetime, timedelta
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class API:
    # Constructor
    def __init__(self):
        self.url = "https://api.messari.io/"
        self.headers = {
            "accept": "application/json",
            "x-messari-api-key": os.environ.get("API_KEY_MESSARI"),
        }
        # self.last_halving = datetime.datetime(2024, 4, 20)
        self.last_halving = datetime.strptime("20/04/2024", "%d/%m/%Y")

    def get_time_series(self, coin_id: str):
        start_time, end_time = self.__get_start_end()

        endpoint = f"marketdata/v1/assets/{coin_id}/price/time-series?interval=1d&startTime={start_time}&endTime={end_time}"
        response = requests.get(self.url + endpoint, headers=self.headers)
        print("request .... : ", response)
        return response.json()["data"]

    def __get_start_end(self):
        # Obtener la hora actual en UTC
        time_now_utc = datetime.now().timestamp()

        # Calcular 150 días antes del último halving en UTC
        time_150days_before_halving = (
            self.last_halving - timedelta(days=250)
        ).timestamp()

        return int(time_150days_before_halving), int(time_now_utc)
