from flask import Blueprint

# Create the Blueprint
auth = Blueprint(
    'auth',       # Blueprint name
    __name__,     # Use __name__ so template_folder works correctly
    template_folder='templates'
)

# Import routes after Blueprint is created
from . import routes
