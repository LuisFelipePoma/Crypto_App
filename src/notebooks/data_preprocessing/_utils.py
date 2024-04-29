import json
import os
import pandas as pd

# -------------------------------------------------- Funciones para la lectura y guardado de archivos -----------------------------

# # Función para guardar los datos en un archivo JSON
# def save_json(FILE: dict | list[dict], dir: str):
#     dirs = dir.split("/")[:-1]
#     if dirs:
#         # Crear un directorio para guardar los metadatos
#         os.makedirs("/".join(dirs), exist_ok=True)

#     # Guardamos las categorias filtradas
#     with open(dir, "w") as file:
#         json.dump(FILE, file)


# Función para leer un archivo JSON
def read_json(file):
    with open(file) as f:
        return json.load(f)


# ---------------------------------------------------- Funciones para preprocesar los Dataframes -------------------------------------


def find_columns_with_nulls(df: pd.DataFrame) -> list[tuple[str, int]]:
    """
    Encuentra las columnas que tienen valores nulos en un DataFrame junto con la cantidad
    """
    # Encuentra las columnas que tienen valores nulos en un DataFrame junto con la cantidad de nulos
    columns: list[str] = df.columns[df.isnull().any()].tolist()
    nulls: list[int] = df[columns].isnull().sum().tolist()
    return list(zip(columns, nulls))
