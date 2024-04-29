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
