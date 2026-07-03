from flask import Flask
from auth import auth

app = Flask(__name__)

# Register the Blueprint
app.register_blueprint(auth)

if __name__ == "__main__":
    app.run(debug=True)

#project/
# │── app.py
# │── config.py
# │── requirements.txt
# │── /static
# │── /templates
# │── /auth
# │     ├── __init__.py
# │     ├── routes.py
# │     └── templates/
# │── /admin
#       ├── __init__.py
#       ├── routes.py
#       └── templates/

# project/
# │── app.py
# │── config.py
# │── extensions.py        # All extensions like db, login_manager, migrate
# │── requirements.txt
# │── instance/
# │── /static
# │── /templates
# │── /models
# │── /services
# │── /auth
# │── /admin
# │── /api
# │── /utils
