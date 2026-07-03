from flask import Flask, request

app = Flask(__name__)

@app.before_request
def before():
    print(f"Visited: {request.path} ({request.method}) {request.user_agent.string}")
    if request.path == "/access":
        if request.args.get("token") != "1234":
            return "you dont have password ** access denide !!! ", 403


@app.after_request
def after(response):
    response.headers["developer"] = "we dont know"
    return response

@app.teardown_request
def teardown(error):
    print(f"some thing is wrong {error}")

@app.get('/')
def home():
    return "home page"

@app.get('/access')
def access():
    return "you have write password"

if __name__ == '__main__':
    app.run(debug=True)