from flask import Flask , request , jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

@app.post('/users')
def create():
    data = request.get_json()
    # name = data.get('name')
    # email = data.get('email')
    user = User(name = data['name'] , email = data['email'])
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "message": "User created successfully"
    }), 201

@app.get('/users')
def all_user():
    data = User.query.all()
    render = [
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
        }
        for u in data
    ]
    return render

@app.get('/users/<int:id>')
def one_user(id):
    # user = User.query.get_or_404(id)
    user = User.query.get(id)

    if not user:
        return {"message": "user not found"}, 404

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
    })

@app.put('/update_users/<int:id>')
def update(id):
    user = User.query.get_or_404(id)
    data = request.get_json()

    user.name = data['name']
    user.email = data.get('email')
    db.session.commit()

    return jsonify({"message": "Updated", "id": user.id})

@app.delete('/delete_users/<int:id>')
def delete(id):
    user=User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Updated", "id": user.id})



with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)