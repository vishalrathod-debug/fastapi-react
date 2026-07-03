
from flask import Flask, render_template ,request,jsonify,abort

app =  Flask(__name__)

@app.get('/')
def home():
    return " home page "

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

@app.errorhandler(500)
def server_side_error(e):
    return render_template("500.html"),500

@app.get('/admin')
def aadmin():
    abort(403)

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'),403

@app.errorhandler(Exception)
def handle_exception(e):
    # JSON response for API clients
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify(error="Server Error", message=str(e)), 500
    return f"Custom Error: {str(e)}", 500

@app.get("/data")
def data_view():
    data = {"msg": "Hello Vishal"}

    wants_json = request.accept_mimetypes['application/json'] >= \
                 request.accept_mimetypes['text/html']

    if wants_json:
        return jsonify(data)

    return render_template("data.html", data=data)


if __name__ == '__main__':
    app.run(debug=True)