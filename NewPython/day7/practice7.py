from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("app.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------- INSERT USER ----------------------
@app.post("/insert_user")
def insert_user():
    conn = get_db()
    cursor = conn.cursor()

    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    cursor.execute(
        "INSERT INTO users(name, email) VALUES (?, ?)",
        (name, email)
    )

    conn.commit()
    return jsonify({"message": "User inserted successfully"}), 201


# ---------------------- GET ALL USERS ----------------------
@app.get("/get_all_users")
def get_all_users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    users = [dict(row) for row in rows]

    return jsonify(users)


# ---------------------- UPDATE USER ----------------------
@app.put("/update_user/<int:id>")
def update_user(id):
    conn = get_db()
    cursor = conn.cursor()

    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    cursor.execute(
        "UPDATE users SET name=?, email=? WHERE id=?",
        (name, email, id)
    )

    conn.commit()

    if cursor.rowcount == 0:
        return {"error": "User not found"}, 404

    return {"message": "User updated", "id": id, "name": name, "email": email}


# ---------------------- DELETE USER ----------------------
@app.delete("/delete_user/<int:id>")
def delete_user(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id=?", (id,))
    conn.commit()

    if cursor.rowcount == 0:
        return {"error": "User not found"}, 404

    return {"message": "Deleted user", "id": id}


# ---------------------- GET USER BY ID ----------------------
@app.get("/user/<int:id>")
def get_single_user(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id=?", (id,))
    row = cursor.fetchone()

    if not row:
        return {"error": f"User {id} not found"}, 404

    return dict(row)


# ---------------------- GLOBAL 404 HANDLER ----------------------
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Resource not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
