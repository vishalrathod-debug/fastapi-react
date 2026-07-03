from flask import render_template, request
from . import auth

@auth.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Here you can check credentials, e.g., with a database
        return f"Email: {email}, Password: {password}"  # For testing only
    return render_template('login.html')
