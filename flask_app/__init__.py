from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5000"}})
app.secret_key = "ejoej0i0i3jj2"