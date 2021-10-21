from flask import Flask
import os
from scss.compiler import Compiler
from firebase import firebase

basedir = os.getcwd()
print(basedir)

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{basedir}/dev.db"

app.root = os.getcwd().replace("\\", "/")

lines = open(f"{basedir}/db_url.txt").readlines()
firebase_url = lines[0]

app.firebase = firebase.FirebaseApplication(firebase_url, None)
app.scss_path = "static/scss/"

scss_paths = [
	"webapp/" + app.scss_path,
	"webapp/" + app.scss_path + "partials"
]

app.scss_compiler = Compiler(search_path=scss_paths)

from webapp import routes
