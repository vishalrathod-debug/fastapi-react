from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI is working"}

@app.get("/users")
def get_users():
    return [
        {"id": 1, "name": "Vishal"},
        {"id": 2, "name": "Rahul"}
    ]
