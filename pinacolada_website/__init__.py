from flask import Flask
app = Flask(__name__)

from pinacolada_website.views import index
app.register_blueprint(index.mod)