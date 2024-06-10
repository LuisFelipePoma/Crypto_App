# -----------------------------------  Librerias Generales -----------------------------
import os
from functools import reduce
import time

# -----------------------------------  Variables de entorno (API KEYS) -----------------------------
from dotenv import load_dotenv
from enum import Enum

# Cargar las variables de entorno
load_dotenv()
# -----------------------------------  Variables TIME SERIES -----------------------------------


HALVINGS_DATE: list[str] = ["2/12/2012", "2/07/2016", "3/05/2020", "20/04/2024"]

# -----------------------------------  Lectura y Escritura de archivos | Peticiones HTTP -----------------------------
import json
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


# Enum para las APIs
class APIS(Enum):
    COINMARKET = {
        "url": "https://pro-api.coinmarketcap.com/v1/",
        "headers": {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": os.environ.get("API_KEY_COINMARKET"),
        },
    }
    MESSARI = {
        "url": "https://api.messari.io/",
        "headers": {
            "accept": "application/json",
            "x-messari-api-key": os.environ.get("API_KEY_MESSARI"),
        },
    }

    COINGECKO = {
        "url": "https://api.coingecko.com/api/v3/",
        "headers": {
            "accept": "application/json",
            "x-cg-demo-api-key": os.environ.get("API_KEY_GECKO"),
        },
    }


# Función para obtener datos de una API
def fetch_data(api: APIS, uri: str, parameters: dict) -> dict:
    """
    `api` : Usar el `Enum` APIS.COINMARKET o APIS.MESSARI \n
    `uri` : Ingresar la uri de la api "exchange/map" | String\n
    `parameters` : Ingresar parametros de la api\n
    """
    api_ = api.value
    session = Session()
    session.headers.update(api_["headers"])
    try:
        url = api_["url"] + uri
        response = session.get(url, params=parameters)
        if response.status_code != 200:
            return {"data": "No Content"}
        return json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return {"error": e}


# Función para guardar los datos en un archivo JSON
def save_json(FILE: dict | list[dict], dir: str):
    dirs = dir.split("/")[:-1]
    if dirs:
        # Crear un directorio para guardar los metadatos
        os.makedirs("/".join(dirs), exist_ok=True)

    # Guardamos las categorias filtradas
    with open(dir, "w") as file:
        json.dump(FILE, file)


# Función para leer un archivo JSON
def read_json(file):
    with open(file) as f:
        return json.load(f)


# -----------------------------------  Funciones Simples -----------------------------
import re
from datetime import datetime, timedelta


# Crear una expresión regular para coincidir con las palabras clave
def create_regex(words: list[str]):
    # Crear una expresión regular que coincida con cualquier palabra clave
    regex_pattern = r"\b(?:{})\b".format("|".join(words))
    regex = re.compile(regex_pattern, re.IGNORECASE)
    return regex


def get_datetime(date: str) -> datetime:
    return datetime.strptime(date, "%d/%m/%Y")


# Función para obtener el timestamp de una fecha
def get_timestamp(date: datetime) -> int:
    return int(datetime.timestamp(date))


def get_start_end_timestamps(date: str, days: int) -> tuple[int, int]:
    start_date: datetime = get_datetime(date)
    # add X days to the date
    end_date: datetime = start_date + timedelta(days=days)
    return get_timestamp(start_date), get_timestamp(end_date)
