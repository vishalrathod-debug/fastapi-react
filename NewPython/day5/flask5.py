import datetime

from flask import Flask , request ,abort

app = Flask(__name__)

@app.before_request #Runs before every request and before route handlers.
def before():
    print("➡ Before Request:", request.path)

@app.after_request #Runs after a successful request, just before the response is sent.
def after(response):
    print("⬅ After Request:", response.status)
    return response

@app.teardown_request #Runs after the request is completely finished, regardless of errors.
def teardown(error):
    print("🛠 Teardown:", error)

#Custom Middleware (Manual)
# You can intercept & process request without touching routes.

@app.before_request
def block_day():
    today = datetime.datetime.today().weekday()  # 0=Mon, 6=Sun

    if today == 6:  # Sunday
        abort(403)  # block requests
    else:
        print("Today is not Sunday")

@app.before_request
def log():
    print(f"User visited: {request.path},with this method{request.method}")

@app.after_request
def add_header(resp):
    resp.headers["X-Powered-By"] = "Flask Learning Program"
    return resp



if __name__ == '__main__':
    app.run(debug=True)