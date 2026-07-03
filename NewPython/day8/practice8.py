from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prac-orm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # One-to-many relationship
    posts = db.relationship("Post", backref="user", lazy=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

    # Many-to-one relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# ------------------------
# Create User + First Post
# ------------------------
@app.post('/user')
def create_user_and_post():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    name = data.get("name")
    content = data.get("content")

    if not name:
        return jsonify({"error": "Missing 'name' field"}), 400
    if not content:
        return jsonify({"error": "Missing 'content' field"}), 400

    user = User(name=name)
    db.session.add(user)
    db.session.commit()  # commit to get user.id

    post = Post(content=content, user_id=user.id)
    db.session.add(post)
    db.session.commit()

    return jsonify({
        "message": "User and Post created!",
        "user_id": user.id,
        "post_id": post.id
    })


# ------------------------
# Get all posts of a user
# ------------------------
@app.get('/user/<int:user_id>/posts')
def get_user_posts(user_id):
    user = User.query.get_or_404(user_id)

    posts_list = [{"id": p.id, "content": p.content} for p in user.posts]
    first_post_id = posts_list[0]["id"] if posts_list else None

    return jsonify({
        "post_id": first_post_id,
        "user": user.name,
        "posts": posts_list
    })


# ------------------------
# Add More Posts
# ------------------------
@app.post('/add_post')
def add_post():
    data = request.get_json()
    user_id = data.get("user_id")
    content = data.get("content")

    if not user_id or not content:
        return jsonify({"error": "Both 'user_id' and 'content' are required"}), 400

    user = User.query.get_or_404(user_id)

    new_post = Post(content=content, user_id=user.id)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({
        "message": "New post added!",
        "user_id": user.id,
        "user_name": user.name,
        "post_id": new_post.id
    })


# ------------------------
# Initialize DB
# ------------------------
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
