# HTTP Methods Explained (Detailed)
# HTTP methods are the actions you ask a server to perform when interacting with a webpage or API.
# Think of them as verbs that describe what you want to do with data.
#
# 1. GET — Fetch Data
# What it does
# Retrieves data from a server.
# Like reading information.
# Does not change anything on the server.
#import requests
# How it behaves
# Data is sent in the URL (query parameters).
# Safe to repeat (refreshing a GET page won’t cause changes).
# Cacheable (browsers may store the response).
#
# Example
# GET /users
#
#
# The server might respond with a list of users.
#
# Real-life analogy: Asking a librarian to show you a book. You are only viewing.


# 2. POST — Send Data / Create Something

# What it does
# Sends new data to the server.
# Usually used to create something (e.g., a new user, comment, order).
# Can change the server’s state.

# How it behaves
# Data is sent in the request body (not visible in URL).
# Not safe to repeat — refreshing a POST form may create duplicates.
# Cannot be cached by default.
#
# Example
# POST /users
#
#
# Request body:
# {
#   "name": "Alice",
#   "email": "alice@example.com"
# }
#
# Server might create a new user.
# Real-life analogy: Filling out a form and submitting it to register for something.


# 3. PUT — Update Data
# What it does
# Replaces an existing resource with new data.
# Usually updates an entire object.

# How it behaves
# Data sent in the request body.
# If the resource exists → update it.
# If it doesn’t exist → sometimes create it (depends on server design).
#
# Example
# PUT /users/1
#
# Body:
# {
#   "name": "Bob Updated",
#   "email": "bob@newmail.com"
# }
#
# Real-life analogy: Replacing a whole document with a new version.


# 4. DELETE — Remove Data
# What it does
# Deletes a resource on the server.
#
# Example
# DELETE /users/1
#
#
# Real-life analogy: Throwing a file into the trash and removing it.
#
# Summary (Simple Table)
# | Method     | Purpose        | Sends Data? | Changes Server? | Safe to Repeat? |
# | ---------- | -------------- | ----------- | --------------- | --------------- |
# | **GET**    | Fetch data     | ✓ (URL)     | ✗               | ✓               |
# | **POST**   | Create data    | ✓ (body)    | ✓               | ✗               |
# | **PUT**    | Update/replace | ✓ (body)    | ✓               | Usually ✓       |
# | **DELETE** | Delete         | optional    | ✓               | Usually ✓       |


# Focus for Today
# Since you’ll use GET and POST, remember:
# ✔ GET = ask for information
# ✔ POST = send new information

from flask import Flask, request ,render_template

app = Flask(__name__)

@app.route('/',methods =["GET"])
def home():
    return { "message": "Welcome to Day 2 API"} #GET is used to retrieve information.
                                                #You're not sending anything to the server — you’re just asking for data.


@app.route('/user/<name>',methods = ['GET'])
def user(name):
    return {"username":name,"message":f"welcome {name}"}
# ✔ What <name> means:
# This creates a dynamic URL.
# Whatever you put in place of <name> is captured and given to the function.

@app.route('/add', methods=['POST','GET'])
def add():
    # if request.method == 'POST':  # ✅ Check request method correctly
    #     data = request.get_json()  # safer than request.json
    #     if not data:
    #         return {"error": "Invalid JSON"}, 400
    #     a = data.get("a")
    #     b = data.get("b")
    #     return {"result": a + b, "a": a, "b": b}
    #
    # return {"message": "Send POST JSON to this route"}
    if request.method == 'POST':
        # Get data from form
        a = request.form.get("a", type=int)
        b = request.form.get("b", type=int)
        result = a + b
        return render_template("result.html", a=a, b=b, result=result)

        # GET request → show the form page
    return render_template("add.html")

# PowerShell’s Invoke-RestMethod works very similarly:
# Invoke-RestMethod -Uri "http://127.0.0.1:5000/add" `
#   -Method POST `
#   -ContentType "application/json" `
#   -Body '{"a":10,"b":5}'
#
# -Uri → the URL
# -Method POST → send POST request
# -ContentType "application/json" → tell server it’s JSON
# -Body → JSON data
#
# ✅ This is the preferred way on Windows.

if __name__ == '__main__':
    app.run(debug=True)


# ✅ Overview: What This Flask App Does
# This Flask application has 3 API routes:
# /hello — simple GET route
# /user/<name> — GET route with URL parameters
# /add — POST route that receives JSON data
# Each route returns a JSON response.