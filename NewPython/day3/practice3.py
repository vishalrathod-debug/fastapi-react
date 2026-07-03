
# | Method               | When to use                                     | Returns            |
# | -------------------- | ----------------------------------------------- | ------------------ |
# | `request.get_json()` | JSON body (Content-Type: application/json)      | dict or None       |
# | `request.json`       | Same as `get_json()`                            | dict or None       |
# | `request.data`       | Raw request body (bytes)                        | bytes              |
# | `request.form`       | Form data (`application/x-www-form-urlencoded`) | ImmutableMultiDict |
# | `request.args`       | Query parameters in URL (GET requests)          | ImmutableMultiDict |
# | `request.values`     | Query parameters + form data                    | ImmutableMultiDict |

from flask import Flask, request , jsonify

app = Flask(__name__)

@app.get('/hello')
def hello():
    return "HELLOW from flask !!!!"

@app.get('/user/<int:user_id>')
def user(user_id):
    return {"message":f"welcome {user_id}" }

@app.get('/search')
def search():
    data = request.args
    name = data.get('name')
    age = data.get('age')
    return jsonify({"message":"success","name ":name ,"age":age})

@app.post('/login')
def login():
    data = request.json  #Same as `get_json()`
    username = data.get("username")
    password = data.get("password")
    email =  data.get("email")

    if len(username) <= 3:
        return {"message":"username must be greater than 3 latter"}
    if len(str(password)) <=3:
        return {"message":"password must be greater than 3 latter"}
    return jsonify({
        "status": "success",
        "received_email": email
    })


if __name__ == "__main__":
    app.run(debug=True)
