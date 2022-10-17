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
    return render_template("index.html")


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


#Literatura
@app.route('/literatura-tasks', methods =["POST", "GET"])
def literatura_tasks():

    questions = [
        {
            'question': "1) A obra de Gregório de Matos – autor que se destaca na literatura barroca brasileira – compreende?",
            'answers': [
            { 'text': "a) poesia épico-amorosa e obras dramáticas", 'correct': False },
            { 'text': "b) poesia satírica e contos burlescos", 'correct': False },
            { 'text': "c) poesia lírica, de caráter religioso e amoroso, e poesia satírica", 'correct': False },
            { 'text': "d) poesia confessional e autos religiosos", 'correct': True },
            ],
        },
        {
            'question': "2) Escolha a alternativa que completa de forma correta a frase abaixo: A linguagem ________, o paradoxo, ________ e o registro das impressões sensoriais são recursos linguísticos presentes na poesia ________.",
            'answers': [
            { 'text': "a) Zoo", 'correct': False },
            { 'text': "b) Section Eng-Ed", 'correct': True },
            { 'text': "c) At the park", 'correct': False },
            { 'text': "d) None of them", 'correct': False },
            ],
        }, 
        {
            'question': "3) Sobre o classicismo é correto afirmar:",
            'answers': [
            { 'text': "a) Movimento que faz referência aos modelos clássicos greco-romanos.", 'correct': True },
            { 'text': "b) Presença de poemas com versos livres e brancos.", 'correct': False },
            { 'text': "c) Memorial de Aires é um exemplo de romance classicista.", 'correct': False },
            { 'text': "d) Possui uma linguagem informal, com uso de regionalismos.", 'correct': False },
            ],
        },
        {
            'question': "4) No Brasil, o período correspondente ao classicismo europeu foi chamado de",
            'answers': [
            { 'text': "a) Simbolismo", 'correct': False },
            { 'text': "b) Quinhentismo", 'correct': True},
            { 'text': "c) Barroco", 'correct': False },
            { 'text': "d) Os Lusíadas", 'correct': False },
            ],
        },
        {
            'question': "5) Um dos maiores autores de língua portuguesa, Luís Vaz de Camões, escreveu obras no período classicista. Uma delas que se destaca é",
            'answers': [
            { 'text': "a) Odisseia", 'correct': False },
            { 'text': "b) Eneida", 'correct': False},
            { 'text': "c) Os Lusíadas", 'correct': True },
            { 'text': "d) Dom Quixote", 'correct': False },
            ],
        }]

    return render_template("literatura_tasks.html", questions = questions)


@app.route('/literatura-videos', methods =["POST", "GET"])
def literatura_videos():

    videos = [
        {   'title': 'Primeiras noções sobre Teoria da Literatura',
            'link': "https://streamable.com/e/s35jvn"
        },
        {
            'title': 'Introdução a Literatura',
            'link': "https://streamable.com/7hsbh7"
        }]

    return render_template("literatura_videos.html", videos = videos)


#Matematica
@app.route('/matematica-tasks', methods =["POST", "GET"])
def matematica_tasks():

    questions = [
        {
            'question': "what is 10 * 2?",
            'answers': [
            { 'text': "102", 'correct': False },
            { 'text': "210", 'correct': False },
            { 'text': "12", 'correct': False },
            { 'text': "20", 'correct': True },
            ],
        },
        {
            'question': "where can you learn how to be a better technical writer?",
            'answers': [
            { 'text': "Zoo", 'correct': False },
            { 'text': "Section Eng-Ed", 'correct': True },
            { 'text': "At the park", 'correct': False },
            { 'text': "None of them", 'correct': False },
            ],
        }]

    return render_template("matematica_tasks.html", questions = questions)

@app.route('/matematica-videos', methods =["POST", "GET"])
def matematica_videos():

    videos = [
        {   'title': 'Primeiras noções sobre Teoria da Literatura',
            'link': "https://streamable.com/e/s35jvn"
        },
        {
            'title': 'Primeiras noções sobre Teoria da Literatura',
            'link': "https://streamable.com/e/s35jvn"
        }]

    return render_template("matematica_videos.html", videos = videos)


#Ciencia
@app.route('/ciencia-tasks', methods =["POST", "GET"])
def ciencia_tasks():

    questions = [
        {
            'question': "1) what is 10 * 2?",
            'answers': [
            { 'text': "102", 'correct': False },
            { 'text': "210", 'correct': False },
            { 'text': "12", 'correct': False },
            { 'text': "20", 'correct': True },
            ],
        },
        {
            'question': "2) where can you learn how to be a better technical writer?",
            'answers': [
            { 'text': "Zoo", 'correct': False },
            { 'text': "Section Eng-Ed", 'correct': True },
            { 'text': "At the park", 'correct': False },
            { 'text': "None of them", 'correct': False },
            ],
        }]

    return render_template("ciencia_tasks.html", questions = questions)


@app.route('/ciencia-videos', methods =["POST", "GET"])
def ciencia_videos():

    videos = [
        {   'title': 'Primeiras noções sobre Teoria da Literatura',
            'link': "https://streamable.com/e/s35jvn"
        },
        {
            'title': 'Primeiras noções sobre Teoria da Literatura',
            'link': "https://streamable.com/e/s35jvn"
        }]

    return render_template("ciencia_videos.html", videos = videos)

#Arte
@app.route('/artes-tasks', methods =["POST", "GET"])
def artes_tasks():

    questions = [
        {
            'question': "1) Marque a opção que não pode ser identificada como  uma obra de arte em nosso dia-a-dia:",
            'answers': [
            { 'text': "a) Cadeira - móveis", 'correct': False },
            { 'text': "b) Igreja - construções", 'correct': False },
            { 'text': "c) Árvore – natureza", 'correct': False },
            { 'text': "d) Nenhuma das alternativas acima", 'correct': True },
            ],
        },
        {
            'question': "2) Qual foi o Ápice do fama de Tarsila do Amaral",
            'answers': [
            { 'text': "Opea de arame", 'correct': False },
            { 'text': "Semana de arte moderna de 22", 'correct': True },
            { 'text': "Crítica feita por Monteiro Lobato", 'correct': False },
            { 'text': "Sua ida a França", 'correct': False },
            ],
        }]

    return render_template("artes_tasks.html", questions = questions)

@app.route('/artes-videos', methods =["POST", "GET"])
def artes_videos():

    videos = [
        {   'title': 'O que é Arte?',
            'link': "https://streamable.com/5pyd03"
        },
        {
            'title': 'Introdução a Arte',
            'link': "https://streamable.com/46ndlw"
        }]

    return render_template("artes_videos.html", videos = videos)

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)