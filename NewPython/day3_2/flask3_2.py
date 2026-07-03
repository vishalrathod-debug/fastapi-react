from flask import Flask , render_template , request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        email = request.form.get('email')

        return render_template('userinfo.html', name=name, age=age, email=email)

    return render_template('home.html')

@app.get('/profile')
def profile():
    profile_data = {                        #Why use ** ?
        "name": "Vishal",                 #Saves you from writing many variables individually.
        "age": 21,                             #Works well when you have lots of data.
        "email": "vishal@example.com",           #Keeps code clean and readable.
        "items": ["Laptop", "Phone", "Tablet"],
        "skills": ["Python", "Flask", "HTML"]
    }
    return render_template('profile.html',**profile_data)

if __name__ == '__main__':
    app.run(debug=True)