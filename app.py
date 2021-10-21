from flask import Flask, render_template,request, session,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

db = SQLAlchemy()

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/Resume"
app.config['SECRET_KEY'] = "anything"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/", methods=['GET','POST'])
def index():
    if session.get('username'):
        return render_template("index.html")
    else:
        return redirect(url_for("login"))
@app.route("/login",methods=['POST','GET'])
def login():
    msg = "Login to your Account"
    if session.get('username'):
        return redirect(url_for('index'))
    elif request.method=="POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username.lower()=="saddique" and password=="saddique":
            session['username']= username
            return redirect(url_for("index"))
        else:
            msg = "Incorrect username and password!"
            return render_template("login.html",msg = msg)
    else:
        return render_template("login.html",msg = msg)
@app.route("/logout")
def logout():
    session.pop('username',None)
    return redirect(url_for('login'))

class Resume(db.Model):
    __tablename__ = "info"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(45), nullable=False, unique=True)
    dob = db.Column(db.DATE, nullable=False)
    experience = db.Column(db.String(200), nullable=False)
    number = db.Column(db.String(15), nullable=False)
    about = db.Column(db.String(250), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    interests = db.Column(db.String(250), nullable=False)
    education = db.Column(db.String(250), nullable=False)
    skills = db.Column(db.String(250), nullable=False)
    awards = db.Column(db.String(250), nullable=False)
@app.route("/createresume", methods=['GET', 'POST'])

def create_resume():
    if request.method == "POST":
        first_name = request.form.get("firstname") # this firstname is getting from html input
        last_name = request.form.get("lastname")
        email = request.form.get("email")
        dob = request.form.get("DOB")
        expr = request.form.get("experience")
        num = request.form.get("number")
        about = request.form.get("about")
        address = request.form.get("address")
        skills = request.form.get("skills")
        interests = request.form.get("interests")
        education= request.form.get("educaion")
        awards = request.form.get("awards")
        print(first_name, last_name, email,about,dob, expr,num,about,address,skills,interests,education,awards,sep=", ")

        record = Resume(first_name=first_name, last_name=last_name, email=email, dob=dob, experience=expr, number=num, about=about,address=address,skills=skills,interests=interests,education=education,awards=awards)
        print(record)
        db.session.add(record)
        db.session.commit()
        
        resume = Resume.query.filter(Resume.email == email).first()
        return render_template("viewresume.html", resume=resume)
    return render_template("createresume.html")


@app.route("/searchresume", methods=['GET', 'POST'])
def searchresume():
    if request.method == "POST":
        email = request.form.get("email")
        find_resume = Resume.query.filter(Resume.email == email).first()
        if find_resume:
            return render_template("viewresume.html", resume=find_resume)
        else:
            return "<h3>No Resume found on this email kindly create another one</h3><br><a href="/{{url_for('createresume')}}/">Create Your Resume</a>"
    return render_template("searchresume.html")


@app.route("/viewresume", methods=['GET'])
def viewresume():
    return render_template("viewresume.html")
if __name__ == "__main__":
    app.run(debug=True)
