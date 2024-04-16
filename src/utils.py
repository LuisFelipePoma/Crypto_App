from dotenv import load_dotenv
import re
import os
import json
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from enum import Enum
from datetime import date
import pandas as pd
import random

load_dotenv()


# Las categorias a buscar
CATEGORIES = ["memes", "game", "gaming", "ai", "real world assets"]

# Crear una expresión regular que coincida con cualquier palabra clave
regex_pattern = r"\b(?:{})\b".format("|".join(CATEGORIES))
regex = re.compile(regex_pattern, re.IGNORECASE)


# Función para imprimir los datos de una forma más legible
def pretty_print(data):
    print(json.dumps(data, indent=2))


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


# Función para obtener datos de una API
# api = Usar Enum APIS
# uri = uri de la API
# parameters = parámetros de la API
def fetch_data(api: APIS, uri: str, parameters: dict) -> dict:
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




def generate_rgb():
    # Generar valores RGB aleatorios
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    
    # Convertir los valores RGB a formato hexadecimal
    color_hex = "#{:02x}{:02x}{:02x}".format(r, g, b)
    
    return color_hex