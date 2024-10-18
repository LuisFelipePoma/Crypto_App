from importlib import metadata
from flask import Flask, json, render_template, request
from services.coins import Coins

# load environment variables
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


# <--------------- home
@app.route("/")
def home():
    general_coins = coins.get_coins_by_mark(500)
    low_coins = coins.get_coins_by_mark(500, True)
    return render_template(
        "index.html", general_coins=general_coins, low_coins=low_coins
    )


# <--------------- APIS
@app.route("/predict", methods=["POST"])
def predict():
    # get the body
    body = request.json
    # get the coin
    data = coins.get_series_by_coin(body["coinId"])  # type: ignore
    predict, metadata = coins.predictRF(data)
    print(predict)
    return json.dumps({"data": data, "predict": int(predict), "metadata": metadata})


@app.route("/search", methods=["POST"])
def search():
    # get the body
    body = request.json
    # get the coin
    print(body)
    query = body["query"]  # type: ignore
    if not query:
        response = coins.get_coins_by_mark(100)
    else:
        response = coins.get_coins_search(query)  # type: ignore
    return json.dumps({"data": response})


@app.route("/low", methods=["GET"])
def low():
    response = coins.get_coins_by_mark(10, True)
    return json.dumps({"data": response})


# <--------------- MAIN
if __name__ == "__main__":
    coins = Coins()
    app.run(host="0.0.0.0")
