import os

from flask import Flask
from flasgger import Swagger

app = Flask(__name__)
port = int(os.getenv('PORT', 5000))
Swagger(app)

from app import api
from serviceMgt import abacus_helper
abacus_helper()
