from datetime import timedelta
from pickletools import read_uint1
from urllib import response
from flask import *
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import urllib.request, json
import requests
import pymysql
from flaskext.mysql import MySQL


app = Flask(__name__)
CORS(app) ## To allow direct AJAX calls

app.secret_key = "Secrect Key"
app.permanent_session_lifetime = timedelta(minutes=120)

mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'thoth'
mysql.init_app(app)


@app.route('/register', methods=['POST'])

def create_user():
    print(request.json)
    if(request.method == "POST"):
        response = jsonify("Sucesso")
        response.status_code = 201
        return response
    else:
        return False
    

@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response

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
    if request.method == 'POST' and request.form['pass'] == 'jtp': 
        session.permanent = True
        user = request.form["email"]
        session["user"] = user 
        return redirect(url_for("user"))  
    else: 
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html") 

@app.route('/user')  
def user(): 
    if "user" in session:
        user = session["user"] 
        return render_template("students.html", user=user) 
    else:
        return redirect(url_for("login")) 


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route('/step-1', methods =["POST", "GET"])  
def step_1():  
    return render_template("step_1.html")


@app.route('/form_student', methods =["POST", "GET"])  
def form_student():
    print(request.form)  
    return render_template("form_student.html")


@app.route('/validate_group', methods = ["POST"])  
def step_2(): 
    print(request.form['groups'])

    if request.method == 'POST' and request.form['groups'] == 'estudante':  
        return redirect(url_for("form_student"))  
    return render_template("form_teacher.html")    


@app.route('/success', methods =["POST", "GET"])  
def modal_success():  
    return render_template("modal_success.html")



@app.route('/tasks-list', methods =["POST", "GET"])
def tasks_student():
    return render_template("tasks_list.html")



if __name__ == '__main__':
	app.run(debug=True)