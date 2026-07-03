# 1️⃣ Client (Frontend)

# What the user sees (website, app).

# Sends requests to the backend.

# 2️⃣ Server (Backend)

# Receives the request from the client.

# Runs Python code (or other server code).

# Decides what data is needed.

# Sends a response back to the client.

# 3️⃣ Database

# Stores information (users, messages, products, etc.).

# Backend communicates with it to read or write data.


from flask import Flask

app = Flask(__name__)

@app.route('/')
def home() :
    return {"message": "Hello, Backend Developer!"}

@app.route('/about')
def about() :
    return {"info": "This is your first Flask API!"}

if __name__ == '__main__' :
    app.run(debug=True)
