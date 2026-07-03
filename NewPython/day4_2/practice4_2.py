from flask import Flask , make_response ,request

app = Flask(__name__)

@app.route('/')
def counter():
    count = request.cookies.get("visit_count")
    if count:
        count = int(count) + 1  # Increase count
    else:
        count = 1  # First visit

    resp = make_response(f"You have visited this site {count} times.")
    resp.set_cookie('visit_count',str(count))

    return resp


@app.route('/set-theme/<theme>')
def set_theme(theme):
    theme = theme.lower()

    if theme not in ['dark', 'light']:
        return "Invalid theme! Use 'dark' or 'light'.", 400

    # Create response message
    resp = make_response(f"Theme set to {theme}")

    # Store theme in cookie
    resp.set_cookie('theme', theme)

    return resp


@app.route('/get-theme')
def get_theme():
    theme = request.cookies.get('theme', 'not set')
    return f"Current theme is: {theme}"

    resp = make_response(f"You have visited this site {count} times.")
    resp.set_cookie('visit_count', str(count))

if __name__ == '__main__':
    app.run(debug=True)