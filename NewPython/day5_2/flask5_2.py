#| Concept              | When it Runs                | Purpose              |
#| -------------------- | --------------------------- | -------------------- |
#| **before_request**   | Before route                | Block, auth, logging |
#| **after_request**    | After route                 | Headers, logging     |
#| **teardown_request** | After request (even errors) | Cleanup              |
#| **middleware**       | Before Flask                | Security, filtering  |

from flask import Flask, request, Response

app = Flask(__name__)

@app.before_request
def before():
    print("Before:", request.path)

    # Blocking a URL
    if "/block" in request.path:
        return "You are blocked!", 403

@app.after_request
def after(response):
    print("After:", response.status_code)
    return response

@app.teardown_request
def teardown(error):
    print("Teardown running...")

class SimpleMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        print("Middleware says hello")
        return self.app(environ, start_response)

app.wsgi_app = SimpleMiddleware(app.wsgi_app)

@app.route("/")
def home():
    return "Welcome"

@app.route("/block")
def bad():
    return "You should not reach here"

if __name__ == '__main__':
    app.run(debug=True)
