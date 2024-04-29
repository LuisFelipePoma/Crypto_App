# -----------------------------------  Librerias Generales -----------------------------
import os
from datetime import date
from functools import reduce
import time
from typing import Callable

# -----------------------------------  Variables de entorno (API KEYS) -----------------------------
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()


# -----------------------------------  Lectura y Escritura de archivos | Peticiones HTTP -----------------------------
import json
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from enum import Enum


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
        response = session.get(api_["url"] + uri, params=parameters)
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

# Crear una expresión regular para coincidir con las palabras clave
def create_regex(words: list[str]):
    # Crear una expresión regular que coincida con cualquier palabra clave
    regex_pattern = r"\b(?:{})\b".format("|".join(words))
    regex = re.compile(regex_pattern, re.IGNORECASE)
    return regex

# fitler a dict by value
def filter_dict_by_value(dict: dict, func: Callable) -> dict:
    print(dict)
    return {k: v for k, v in dict.items() if func(v)}
