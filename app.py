from flask import *
from flask_restful import Resource, Api
from flask_cors import CORS
import urllib.request, json
import requests

app = Flask(__name__)
CORS(app) ## To allow direct AJAX calls


@app.route("/")
@app.route("/index", methods=["POST", "GET"])
def index():

    limits = [1,2,3,4,5,6]
    pokemons_req = []

    for limit in limits:
        api = f"https://pokeapi.co/api/v2/pokemon/{limit}"
        request = requests.get(api)
        pokemon_load = json.loads(request.content)
        pokemons_req.append(pokemon_load)


    pokemon_json = []
    for pokemon in pokemons_req:
        pokemon_body = {
            "name": pokemon["name"],
            "sprite": pokemon["sprites"]["back_default"],
            "height": pokemon["height"],
            "weight": pokemon["weight"]
        }
        pokemon_json.append(pokemon_body)
        
    print(pokemon_json)

    list_titles = [{"thead": "Altura"}]

    print(list_titles)

    return render_template("index.html", items = pokemon_json, list_titles = list_titles)


@app.route("/new", methods=["POST", "GET"])
def new():
    return render_template("form.html")



@app.route("/login", methods=["POST", "GET"])
def login():
    return render_template("login.html")



@app.route('/validate', methods = ["POST"])  
def validate():  
    if request.method == 'POST' and request.form['pass'] == 'jtp':  
        return redirect(url_for("home"))  
    return redirect(url_for("login"))  


@app.route('/home')  
def home():  
    return "logged in successfully"  

if __name__ == '__main__':
	app.run(debug=True)