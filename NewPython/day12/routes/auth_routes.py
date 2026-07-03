from flask import Blueprint, request, render_template, redirect, url_for, flash, make_response
from flask_jwt_extended import create_access_token, set_access_cookies  # Added set_access_cookies
from app import db
from models.user import User
from utils.hash import hash_password, verify_password

# Initialize Blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# --- Render HTML Pages ---

@auth_bp.get("/login")
def login_page():
    """Renders the login form page."""
    return render_template("login.html")


@auth_bp.get("/register")
def register_page():
    """Renders the registration form page."""
    return render_template("register.html")


# --- API Endpoints ---

@auth_bp.post("/register")
def register():
    """Handles new user registration form submission."""
    data = request.form
    username = data.get("username")
    password = data.get("password")

    # 1. Check if user already exists
    if User.query.filter_by(username=username).first():
        flash("Username already exists!", "danger")
        return redirect(url_for("auth.register_page"))

    # 2. Create new user and hash password
    # The hash_password utility is crucial for security
    new_user = User(username=username, password_hash=hash_password(password))
    db.session.add(new_user)
    db.session.commit()

    flash("Registration successful! You can now log in.", "success")
    return redirect(url_for("auth.login_page"))


@auth_bp.post("/login")
def login():
    """Handles login form submission and issues a JWT token."""
    data = request.form
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    # 1. Verify credentials
    if not user or not verify_password(user.password_hash, password):
        flash("Invalid credentials", "danger")
        return redirect(url_for("auth.login_page"))

    # 2. Create JWT token
    access_token = create_access_token(identity=user.id)

    # 3. Create response object (redirect to dashboard)
    # The token needs to be set *before* the redirect is returned
    response = redirect(url_for("user.dashboard"))

    # 4. Set the token as an HTTP-only cookie on the response
    set_access_cookies(response, access_token)

    return response