from flask import Flask , request , render_template, redirect , flash ,url_for,session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask (__name__)

app.secret_key = "your_secret_key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prac10-orm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def to_dict(self):
        return{
            "id":self.id,
            "username":self.username
        }

@app.route("/")
def home():
    user = None
    if session.get("user_id"):
        user = User.query.get(session["user_id"])
    return render_template("home.html", title="Home", user=user)


@app.get("/register")
def register_get():
    return render_template("register.html",title="Register")

@app.post("/register")
def register_post():

    data = request.form

    username = data.get("username")
    password = data.get("password")

    # Fix: Proper SQLAlchemy check
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash("Username is not available", "error")
        return redirect(url_for('register_get'))
    password_hash = generate_password_hash(password)
    user = User(username = username ,password = password_hash)
    db.session.add(user)
    db.session.commit()

    flash("user register successful","success")
    return redirect(url_for('login_get'))

@app.get('/login')
def login_get():
    return render_template('login.html')
@app.post('/login')
def login():
    data = request.form

    username = data.get("username")
    password = data.get("password")

    user =  User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        session["user_id"] = user.id
        flash("user logged in successful", "success")
        return redirect(url_for('home'))
    else:
        flash("password is wrong" , "error")
        return redirect(url_for('login_get'))

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Logged out successfully", "success")
    return redirect(url_for("home"))

@app.get('/dashboard')
def dashboard():
    if not session.get("user_id"):
        flash("You must be logged in to access the dashboard", "error")
        return redirect(url_for("login_get"))

    user = User.query.get(session["user_id"])
    return render_template('dashboard.html', user=user)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)