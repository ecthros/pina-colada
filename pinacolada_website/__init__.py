from flask_cors import CORS, cross_origin
from flask import Flask
app = Flask(__name__)
CORS(app)
#app.config["server="]

from pinacolada_website.views import index
#i = index.Index()
app.register_blueprint(index.mod)