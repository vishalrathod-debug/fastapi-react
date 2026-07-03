from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key_here"   # change this in real app


# ------------------------
# Database Helper
# ------------------------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# ------------------------
# Create Users Table
# ------------------------
def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()


init_db()   # create the database if missing


# ------------------------
# Home Page
# ------------------------
@app.route("/")
def home():
    return render_template("base.html", title="Home")


# ------------------------
# Register
# ------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        password_hash = generate_password_hash(password)

        conn = get_db()
        try:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                         (username, password_hash))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Username already exists."
        finally:
            conn.close()

        return redirect("/login")

    return render_template("register.html")


# ------------------------
# Login
# ------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username = ?",
                            (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            return redirect("/dashboard")
        else:
            return "Invalid username or password."

    return render_template("login.html")


# ------------------------
# Dashboard (Protected)
# ------------------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/access-denied")

    return render_template("dashboard.html")


# ------------------------
# Access Denied Page
# ------------------------
@app.route("/access-denied")
def access_denied():
    return render_template("access_denied.html"), 403


# ------------------------
# Logout
# ------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ------------------------
# Run App
# ------------------------
if __name__ == "__main__":
    app.run(debug=True)
