from datetime import timedelta
from flask import *
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import urllib.request, json
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
CORS(app) ## To allow direct AJAX calls

app.secret_key = "Secrect Key"
app.permanent_session_lifetime = timedelta(minutes=120)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thoth.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)


login_manager.login_message = "O usuário precisa estar logado para visualizar esta página"

login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except:
        return None
    
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    cpf = db.Column(db.String(500), nullable=False)
    postcode = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    
    def __init__(self, first_name, last_name, cpf, postcode, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.cpf = cpf
        self.postcode = postcode
        self.email = email
        self.password = password
           
    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)
    
class Questions(db.Model):
    id_question = db.Column(db.Integer, primary_key=True) 
    question = db.Column(db.String(500), nullable=False)
    option_a = db.Column(db.String(500), nullable=False)
    option_b = db.Column(db.String(500), nullable=False)
    option_c = db.Column(db.String(500), nullable=False)
    option_d = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    
    def __init__(self, question, option_a, option_b, option_c, option_d, answer, category):
        self.question = question
        self.option_a = option_a
        self.option_b = option_b
        self.option_c = option_c
        self.option_d = option_d
        self.answer = answer
        self.category = category
        

@app.route('/register', methods=['POST'])
def create_user():
    if request.method == 'POST':
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        cpf = request.form["cpf"]
        postcode = request.form["cep"]
        email = request.form["email"]
        password = request.form["password"]
        user = User(first_name, last_name, cpf, postcode, email, password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('form_student.html')

def get_all_questions():
    questions = Questions.query.all()
    
    return questions
    

@app.route("/")
@app.route("/index", methods=["POST", "GET"])
def index():
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST': 
        session.permanent = True
        email = request.form["email"]
        password = request.form["pass"]
        user = User.query.filter_by(email=email).first()
        if user:
            login_user(user)
            return redirect(url_for("user"))
        else:
             flash("Usuário não encontrado")
        
    return render_template("login.html") 


@app.route('/user', methods=['GET', 'POST'])  
@login_required
def user():
    artes_count = Questions.query.filter_by(category='artes').count()
    matematica_count = Questions.query.filter_by(category='matematica').count()
    literatura_count = Questions.query.filter_by(category='literatura').count()
    ciencia_count = Questions.query.filter_by(category='ciencia').count()
    
    if  session.get("tasks_completed") == None:
        session["tasks_completed"] = 0
        tasks_completed = session["tasks_completed"]
        return render_template("students.html", artes = artes_count, matematica = matematica_count, literatura = literatura_count, ciencia = ciencia_count, tasks_completed = tasks_completed) 

    else:   
        tasks_completed = session["tasks_completed"]
        return render_template("students.html", artes = artes_count, matematica = matematica_count, literatura = literatura_count, ciencia = ciencia_count, tasks_completed = tasks_completed) 


@app.route("/logout")
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("login"))


@app.route('/step-1', methods =["POST", "GET"])  
def step_1():  
    return render_template("step_1.html")


@app.route('/form_student', methods =["POST", "GET"])  
def form_student():
    return render_template("form_student.html")


@app.route('/validate_group', methods = ["POST"])  
def step_2(): 
    if request.method == 'POST' and request.form['groups'] == 'estudante':  
        return redirect(url_for("form_student"))  
    return render_template("form_teacher.html")


#Literatura
@app.route('/literatura-tasks', methods =["POST", "GET"])
@login_required
def literatura_tasks():
    
    questions = [
    {
        'question': "A obra de Gregório de Matos – autor que se destaca na literatura barroca brasileira – compreende?",
        'options': [
        { 'text': "a) poesia épico-amorosa e obras dramáticas", 'alternative': "a" },
        { 'text': "b) poesia satírica e contos burlescos", 'alternative': "b" },
        { 'text': "c) poesia lírica, de caráter religioso e amoroso, e poesia satírica", 'alternative': "c" },
        { 'text': "d) poesia confessional e autos religiosos", 'alternative': "d" },
        ],
        'answer': 'c'
    }]
    
    if request.method == "GET":
        if  session.get("alt_q_validade_literatura") == None and session.get("is_correct_literatura") == None:
            return render_template("literatura_tasks.html", questions = questions)
        else: 
            alt_q_validade = session["alt_q_validade_literatura"]
            is_correct = session["is_correct_literatura"]
            return render_template("literatura_tasks.html", questions = questions, is_correct = is_correct, text = alt_q_validade)
    else:
        if request.form["questions"] == questions[0]["answer"]:
            flash("Parabéns! Resposta correta", 'green')
            res = int(session["tasks_completed"]) + 1
            session["tasks_completed"] = res
            session["is_correct_literatura"] = True
            session["alt_q_validade_literatura"] = questions[0]["answer"]
            return render_template("literatura_tasks.html", questions = questions, is_correct = True, text = questions[0]["answer"])
        else:
            session["is_correct_literatura"] = False
            session["alt_q_validade_literatura"] = questions[0]["answer"]
            flash("Resposta Errada! Caso precise, dê uma olhada nas vídeo aulas", 'red')
            return render_template("literatura_tasks.html", questions = questions, is_correct = False, text = questions[0]["answer"])
        
        
        
@app.route('/literatura-videos', methods =["POST", "GET"])
@login_required
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
@login_required
def matematica_tasks():

    questions = [
        {
            'question': "Some 10 com a resposta de |x|. (x + 10)10/2 = 15/5.",
            'options': [
            { 'text': "a) 12,4", 'alternative': "a" },
            { 'text': "b) 20,3", 'alternative': "b" },
            { 'text': "c) 9,4", 'alternative': "c" },
            { 'text': "d) 19,4", 'alternative': "d" },
            ],
            'answer': "d"
        }]
    
    if request.method == "GET":
        if  session.get("alt_q_validade_matematica") == None and session.get("is_correct_matematica") == None:
            return render_template("matematica_tasks.html", questions = questions)
        else: 
            alt_q_validade = session["alt_q_validade_matematica"]
            is_correct = session["is_correct_matematica"]
            return render_template("matematica_tasks.html", questions = questions, is_correct = is_correct, text = alt_q_validade)
    else:
        if request.form["questions"] == questions[0]["answer"]:
            flash("Parabéns! Resposta correta", 'green')
            res = int(session["tasks_completed"]) + 1
            session["tasks_completed"] = res
            session["is_correct_matematica"] = True
            session["alt_q_validade_matematica"] = questions[0]["answer"]
            return render_template("matematica_tasks.html", questions = questions, is_correct = True, text = questions[0]["answer"])
        else:
            session["is_correct_matematica"] = False
            session["alt_q_validade_matematica"] = questions[0]["answer"]
            flash("Resposta Errada! Caso precise, dê uma olhada nas vídeo aulas", 'red')
            return render_template("matematica_tasks.html", questions = questions, is_correct = False, text = questions[0]["answer"])
        
        
        

@app.route('/matematica-videos', methods =["POST", "GET"])
@login_required
def matematica_videos():

    videos = [
        {   'title': 'Matemática Básica',
            'link': "https://streamable.com/6867ba"
        },
        {
            'title': 'Matemática do Zero',
            'link': "https://streamable.com/fpifqa"
        }]

    return render_template("matematica_videos.html", videos = videos)


#Ciencia
@app.route('/ciencia-tasks', methods =["POST", "GET"])
@login_required
def ciencia_tasks():

    questions = [
        {
            'question': "Como é chamada a propriedade de atrair materiais? ",
            'options': [
            { 'text': "a) Condução", 'alternative': "a" },
            { 'text': "b) Isopropílico", 'alternative': "b" },
            { 'text': "c) Isolante", 'alternative': "c" },
            { 'text': "d) Magnetismo", 'alternative': "d" }, 
            ],
            'answer': 'd'
        }
    ]

    if request.method == "GET":
        if  session.get("alt_q_validade_ciencia") == None and session.get("is_correct_ciencia") == None:
            return render_template("ciencia_tasks.html", questions = questions)
        else: 
            alt_q_validade = session["alt_q_validade_ciencia"]
            is_correct = session["is_correct_ciencia"]
            return render_template("ciencia_tasks.html", questions = questions, is_correct = is_correct, text = alt_q_validade)
    else:
        if request.form["questions"] == questions[0]["answer"]:
            flash("Parabéns! Resposta correta", 'green')
            res = int(session["tasks_completed"]) + 1
            session["tasks_completed"] = res
            session["is_correct_ciencia"] = True
            session["alt_q_validade_ciencia"] = questions[0]["answer"]
            return render_template("ciencia_tasks.html", questions = questions, is_correct = True, text = questions[0]["answer"])
        else:
            session["is_correct_ciencia"] = False
            session["alt_q_validade_ciencia"] = questions[0]["answer"]
            flash("Resposta Errada! Caso precise, dê uma olhada nas vídeo aulas", 'red')
            return render_template("ciencia_tasks.html", questions = questions, is_correct = False, text = questions[0]["answer"])


@app.route('/ciencia-videos', methods =["POST", "GET"])
@login_required
def ciencia_videos():

    videos = [
        {   'title': 'O que são Ciências Naturais',
            'link': "https://streamable.com/cihk8z"
        },
        {
            'title': 'O que são Ciências Sociais',
            'link': "https://streamable.com/t31dpp"
        }]

    return render_template("ciencia_videos.html", videos = videos)

#Arte
@app.route('/artes-tasks', methods =["POST", "GET"])
@login_required
def artes_tasks():

    questions = [
        {
            'question': "Qual foi o Ápice do fama de Tarsila do Amaral",
            'options': [
            { 'text': "Opea de arame", 'alternative': "a" },
            { 'text': "Semana de arte moderna de 22", 'alternative': "b" },
            { 'text': "Crítica feita por Monteiro Lobato", 'alternative': "c" },
            { 'text': "Sua ida a França", 'alternative': "d" },
            ],
            'answer': "b"
        }
    ]
    
    if request.method == "GET":
        if  session.get("alt_q_validade_artes") == None and session.get("is_correct_artes") == None:
            return render_template("artes_tasks.html", questions = questions)
        else: 
            alt_q_validade = session["alt_q_validade_artes"]
            is_correct = session["is_correct_artes"]
            return render_template("artes_tasks.html", questions = questions, is_correct = is_correct, text = alt_q_validade)
    else:
        if request.form["questions"] == questions[0]["answer"]:
            flash("Parabéns! Resposta correta", 'green')
            res = int(session["tasks_completed"]) + 1
            session["tasks_completed"] = res
            session["is_correct_artes"] = True
            session["alt_q_validade_artes"] = questions[0]["answer"]
            return render_template("artes_tasks.html", questions = questions, is_correct = True, text = questions[0]["answer"])
        else:
            session["is_correct_artes"] = False
            session["alt_q_validade_artes"] = questions[0]["answer"]
            flash("Resposta Errada! Caso precise, dê uma olhada nas vídeo aulas", 'red')
            return render_template("artes_tasks.html", questions = questions, is_correct = False, text = questions[0]["answer"])
                

@app.route('/artes-videos', methods =["POST", "GET"])
@login_required
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
    app.run()