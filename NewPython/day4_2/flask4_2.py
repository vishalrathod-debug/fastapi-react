from flask import Flask, url_for, redirect, make_response ,request ,Response

app = Flask(__name__)

@app.get('/')
def home():
    url = url_for('about')  # Generate a URL for the "about" function
    return f"<a href='{url}'>go to about page</a>"

@app.get('/about')
def about():
    return "this is about page"

@app.route('/user/<name>')
def user(name):
    return f"HELLO {name}"

@app.route('/go-to-user')
def go_to_user():
    return redirect(url_for('user',name="Vishal"))

#Custom Response Object
# @app.get('/custom')
# def custom():
#     response = make_response("this is a custom response",200)
#     response.headers["X-Custom-Header"] = "MyValue"
#     return response

@app.get('/custom')
def custom():
    return Response("this is from custom response class ",status=201,mimetype="text/plain")

@app.route('/setcookies')
def setcookies():
    resp = make_response("Cookie set!")
    resp.set_cookie("username","jon")
    return resp

@app.route('/getcookies')
def getcookie():
    username = request.cookies.get('username')
    return f"Username from cookie is: {username}"



if __name__ == '__main__':
    app.run(debug=True)