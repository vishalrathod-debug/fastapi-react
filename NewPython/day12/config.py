#
#

import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwtsecretkey")
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# 1. import os
#
# Used to read environment variables.
#
# Lets you override secret keys without hardcoding them.
#
# 🔐 2. SECRET_KEY
# SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
#
#
# Flask uses this for securely signing session cookies.
#
# Loaded from an environment variable (SECRET_KEY).
#
# If not set, it uses "supersecretkey" as fallback.
#
# 🔑 3. JWT_SECRET_KEY
# JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwtsecretkey")
#
#
# This key signs and verifies JWT tokens.
#
# Should be long and random in production.
#
# 🗃️ 4. SQLALCHEMY_DATABASE_URI
# SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
#
#
# Tells SQLAlchemy to use SQLite and store the database in a file called data.db.
#
# If the project is run from root folder:
#
# flask_jwt_auth/data.db
#
# ⚙️ 5. SQLALCHEMY_TRACK_MODIFICATIONS
# SQLALCHEMY_TRACK_MODIFICATIONS = False
#
#
# Disables SQLAlchemy's event tracking system to save memory.
#
# Recommended to keep this False.