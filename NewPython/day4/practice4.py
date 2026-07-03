from flask import Flask,request,flash,render_template,redirect,url_for

app = Flask(__name__)
app.secret_key="practice4"

@app.get('/contact')
def show_form():
    return render_template('contact.html')


@app.post('/contact')
def contact():
    name = request.form.get("name").strip()
    email = request.form.get("email").strip()
    msg = request.form.get("message").strip()

    if not name or not email or not msg:
        flash("every thing is needed","error")
        return redirect(url_for('show_form'))

    return f"Thank you {name}, we received your message."

@app.get('/login')
def show_login():
    return render_template('login.html')

@app.post('/login')
def login():
    password = request.form.get("password", "").strip()  # safe, default to empty string
    if len(password) < 4:
        flash("Password must be at least 4 characters long", "error")
        return redirect(url_for('show_login'))
    return "welcome you are logged in"


if __name__ == '__main__':
    app.run(debug=True)