from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

@app.before_request
def before():
    print(f"visited: {request.path} ({request.method})")
    # print(request.args.get("key"))
    # if not request.args.get("key") :
    #     return ("access denied ")

@app.before_request
def check_specific_page():
    if request.path == "/secret":
        if request.cookies.get("key") != "123":
            return jsonify({"error": "Access denied"}), 403

@app.get('/')
def home():
    resp = make_response("set key")
    resp.set_cookie("key" , "123")
    return resp

@app.route("/secret")
def secret():

    return "This is the secret page!"

if __name__ == '__main__':
    app.run(debug=True)