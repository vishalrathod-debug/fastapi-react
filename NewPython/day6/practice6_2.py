from flask import Flask, request
import sqlite3 as sql

app = Flask(__name__)
DB_FILE = "app.db"

# ------------------------
# Database utility functions
# ------------------------
def get_db():
    conn = sql.connect(DB_FILE)
    conn.row_factory = sql.Row
    return conn

def init_db():
    """Initialize the database and create users table if it does not exist."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            );
        """)
        conn.commit()

# ------------------------
# Routes / CRUD Operations
# ------------------------

@app.post("/user")
def create_user():
    data = request.json
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return {"error": "Name and email are required"}, 400

    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
            conn.commit()
        return {"message": "User created"}, 201
    except sql.IntegrityError:
        return {"error": "Email already exists!"}, 400

@app.get("/users")
def get_users():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

@app.get("/user/<int:id>")
def get_user(id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id=?", (id,))
        row = cursor.fetchone()
        if not row:
            return {"error": "User not found"}, 404
        return dict(row)

@app.put("/user/<int:id>")
def update_user(id):
    data = request.json
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return {"error": "Name and email are required"}, 400

    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET name=?, email=? WHERE id=?", (name, email, id))
            if cursor.rowcount == 0:
                return {"error": "User not found"}, 404
            conn.commit()
        return {"message": "User updated"}
    except sql.IntegrityError:
        return {"error": "Email already exists!"}, 400

@app.delete("/user/<int:id>")
def delete_user(id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=?", (id,))
        if cursor.rowcount == 0:
            return {"error": "User not found"}, 404
        conn.commit()
    return {"message": "User deleted"}

# ------------------------
# Run the Flask app
# ------------------------
if __name__ == '__main__':
    # Initialize database BEFORE running the app
    init_db()
    app.run(debug=True)
