"""Module os used in order to use SECRET_KEY and Flask module to run HTML via flask."""
from os import getenv
from flask import Flask

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes
# End-of-file (EOF)