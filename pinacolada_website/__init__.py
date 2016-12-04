from flask_cors import CORS, cross_origin
from flask import Flask
from pinacolada_website.views import index

app = Flask(__name__)
CORS(app)
app.register_blueprint(index.mod)
