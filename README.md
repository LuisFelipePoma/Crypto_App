# Crypto

# How to use

## Create the file `.env` on the folder `src` Set the environment variables

```bash
# .env file
API_KEY_COINMARKET="your-key-api"
API_KEY_MESSARI="your-key-api"
```

## Install the dependencies of `requirements.txt`

```bash
pip install -r requirements.txt
```



obtener data en plazos de inicio de halving hasta fin de halving

1. dividir la data en dos periodos
   1. periodo 1: inicio del halving
   2. periodo 2: auge de la monedas durante el resto del halving
2. entrenar el modelo en base a el primer periodo y predecir el resultado si en el segundo periodo la moneda superara su precio