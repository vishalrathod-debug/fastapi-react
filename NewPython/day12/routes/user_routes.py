from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.get("/dashboard")
@jwt_required(optional=True)
def dashboard():
    return render_template("dashboard.html")

@user_bp.get("/profile")
@jwt_required(optional=True)
def profile():
    user_id = get_jwt_identity()
    return render_template("profile.html", user_id=user_id)
