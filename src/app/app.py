from flask import Flask, json, render_template, request, send_from_directory
from services.coins import Coins

# load environment variables
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


# <--------------- home
@app.route("/")
def home():
    coins_bubbles = coins.get_coins_list(100)
    return render_template("index.html", coins_bubbles=coins_bubbles)


# <--------------- APIS
@app.route("/predict", methods=["POST"])
def predict():
    # get the body
    body = request.json
    # get the coin
    response = coins.get_series_by_coin(body["coinId"])  # type: ignore
    return json.dumps({"data": response})


@app.route("/search", methods=["POST"])
def search():
    # get the body
    body = request.json
    # get the coin
    print(body)
    query = body["query"]  # type: ignore
    if not query:
        response = coins.get_coins_list(100)
    else:
        response = coins.get_coins_search(query)  # type: ignore
    return json.dumps({"data": response})

# @app.route("/best", methods=["GET"])
# def best_coins():
#     return 

# @app.route("/worst", methods=["GET"])
# def worst_coins():
#     return 

# <--------------- MAIN
if __name__ == "__main__":
    coins = Coins()
    app.run(host="0.0.0.0", port=5000, debug=True)
