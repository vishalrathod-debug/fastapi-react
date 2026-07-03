from flask import Flask, request, render_template, redirect, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prac9-orm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# ----------------------------------------------------
# MODELS
# ----------------------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    def to_dict(self):
        return {"id": self.id, "name": self.name}


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "user_id": self.user_id
        }


# ----------------------------------------------------
# LOGGING
# ----------------------------------------------------
@app.before_request
def log_request():
    print(f"[LOG] Visiting {request.method} {request.path}")


@app.after_request
def add_custom_header(response):
    response.headers["X-App-Name"] = "DemoApp-SQLAlchemy"
    return response


# ----------------------------------------------------
# HOME PAGE
# ----------------------------------------------------
@app.get("/")
def home():
    users = User.query.all()
    posts = Post.query.all()
    return render_template("home.html", users=users, posts=posts)


# ----------------------------------------------------
# CREATE USER
# ----------------------------------------------------
@app.post("/users")
def create_user():
    data = request.get_json()

    if not data or "name" not in data:
        return {"error": "name is required"}, 400

    usr = User(name=data["name"])
    db.session.add(usr)
    db.session.commit()

    return jsonify({
        "message": "User added successfully!",
        "user": usr.to_dict()
    }), 201


# ----------------------------------------------------
# CREATE POST
# ----------------------------------------------------
@app.post("/posts")
def create_post():
    data = request.get_json()

    # Required fields
    if not data or "title" not in data or "content" not in data or "user_id" not in data:
        return {"error": "title, content, user_id required"}, 400

    # Check if user exists
    user = User.query.get(data["user_id"])
    if not user:
        return {"error": "User not found"}, 404

    post = Post(
        title=data["title"],
        content=data["content"],
        user_id=data["user_id"]
    )

    db.session.add(post)
    db.session.commit()

    return jsonify({
        "message": "Post created successfully!",
        "post": post.to_dict()
    }), 201


# ----------------------------------------------------
# GET ALL USERS
# ----------------------------------------------------
@app.get("/users")
def get_all_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


# ----------------------------------------------------
# UPDATE USER
# ----------------------------------------------------
@app.put("/users/<int:user_id>")
def update_user(user_id):
    usr = User.query.get_or_404(user_id)
    data = request.get_json()

    usr.name = data.get("name", usr.name)
    db.session.commit()

    return jsonify(usr.to_dict())


# ----------------------------------------------------
# DELETE USER (with redirect)
# ----------------------------------------------------
@app.delete("/users/<int:user_id>")
def delete_user(user_id):
    usr = User.query.get_or_404(user_id)

    db.session.delete(usr)
    db.session.commit()

    # Requirement: redirect after delete
    return redirect(url_for("get_all_users"))


# ----------------------------------------------------
# START APP
# ----------------------------------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
