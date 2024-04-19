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


# -----------------------------------  Creacion y Visualizacion del grafo -----------------------------

import networkx as nx
import matplotlib.pyplot as plt
from pylab import rcParams
import numpy as np


# Funcion para graficar los Grafos
def show_graph(
    G: nx.DiGraph | nx.Graph,
    figure_size: tuple[int, int] = (20, 20),
    scale: int = 20,
    k_spring_layout: int = 10,
    colors: list[str] = [],
    node_size: int = 50,
    iterations: int = 3,
    edgelists: list[tuple[list[tuple[str, str]], str]] = [],
):
    # ------------ VALIDAR PARAMS NULOS o VACIOS

    # Se generan los colores de los nodos
    useArrow = True if type(G) == nx.DiGraph else False
    colors = [generate_rgb() * G.order()] if not colors else colors
    edgelists = [(G.edges(), "k")] if not edgelists else edgelists

    # ------------ GRAFICAR EL GRAFO

    # Se setea el tamaño de la figura
    rcParams["figure.figsize"] = figure_size

    # Se obtienen las posiciones de los nodos
    pos_xy = nx.spring_layout(
        G, scale=scale, k=k_spring_layout / np.sqrt(G.order()), iterations=iterations
    )

    # Obtener el grado de los nodos
    degrees = dict(G.degree)  # type: ignore

    # Se obtienen los tamaños de los nodos
    node_sizes = [degrees[node] * node_size for node in degrees]

    # Se dibuja el grafo
    fig = plt.figure(frameon=False)
    ax = fig.add_axes((0, 0, 1, 1))
    ax.axis("off")

    # Se dibujan los nodos
    nx.draw_networkx_nodes(
        G,
        pos_xy,
        node_color=colors,  # type: ignore
        node_size=node_sizes,  # type: ignore
        alpha=0.7,
        edgecolors="black",
        margins=(0, 0),
    )

    # Se dibujan las etiquetas
    nx.draw_networkx_labels(
        G,
        pos_xy,
        font_size=10,
        font_color="black",
        clip_on=False,
        alpha=0.9,
        font_family="monospace",
    )

    # Se dibujan las aristas
    for edgelist, color in edgelists:
        nx.draw_networkx_edges(
            G,
            pos_xy,
            edgelist=edgelist,
            width=0.2,
            style="-",
            edge_color=color,
            alpha=0.5,
            arrows=useArrow,
            connectionstyle="Arc3,rad=0.4",
        )


# -----------------------------------  Funciones Simples -----------------------------
import re
import random


# Función para generar un color RGB aleatorio
def generate_rgb():
    # Generar valores RGB aleatorios
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    # Convertir los valores RGB a formato hexadecimal
    color_hex = "#{:02x}{:02x}{:02x}".format(r, g, b)

    return color_hex


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
