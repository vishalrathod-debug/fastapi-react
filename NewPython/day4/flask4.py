from flask import Flask , request , render_template, flash ,redirect , url_for

app = Flask(__name__)
app.secret_key = "newkeyday4"

@app.get('/register')
def show_form():
    return render_template('register.html')

@app.post('/register')
def register():
    form_data = request.form.to_dict()
    name = form_data.get("name").strip()
    age = form_data.get("age",10)

    if not age or not name:
        flash("Age and Name must be pass", "error")
        return redirect(url_for('show_form'))

    return form_data



if __name__== '__main__':
    app.run(debug=True)