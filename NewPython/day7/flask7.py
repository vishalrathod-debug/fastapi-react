from flask import Flask ,request , jsonify
import sqlite3

app = Flask(__name__)

def db_connect():
    conn = sqlite3.connect("app.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.post('/getuser')
def get_user():
    con = db_connect()
    curses = con.cursor()
    data = request.get_json()
    name= data.get('name')
    email = data.get('email')

    curses.execute("INSERT INTO users(name , email) VALUES(?,?)",(name,email))

    con.commit()
    return {"message": "User created"}, 201

@app.get('/showuser')
def show_user():
    con = db_connect()
    curses = con.cursor()
    curses.execute("SELECT * FROM users")
    rows = curses.fetchall()
    users = [dict(row) for row in rows]

    return jsonify(users)

@app.get('/getuser_withid')
def get_useer_with_id():
    _id = request.args.get("id")
    con = db_connect()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?",(_id,))
    row = cursor.fetchone()

    if not row:
        return {"error": "User not found"}, 404

    return dict(row)

@app.post("/users/<int:id>")
def update_user(id):
    data = request.json
    name = data.get("name")
    email = data.get("email")

    conn = db_connect()
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET name=?, email=? WHERE id=?", (name, email, id))
    conn.commit()

    return {"message": "Updated"}

@app.delete("/delete_user/<int:id>")
def delete_user(id):
    conn = db_connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id=?", (id,))
    conn.commit()

    return {"message": "Deleted"}

@app.errorhandler(sqlite3.IntegrityError)
def handle_db_error(e):
    return {"error": "Email already exists!"}, 400


if __name__ == '__main__':
    app.run(debug=True)