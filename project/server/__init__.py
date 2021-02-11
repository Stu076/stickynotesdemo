import os

from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
template_dir = os.path.join(template_dir, "project")
template_dir = os.path.join(template_dir, "frontend")
template_dir = os.path.join(template_dir, "templates")

static_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
static_dir = os.path.join(static_dir, "project")
static_dir = os.path.join(static_dir, "frontend")
static_dir = os.path.join(static_dir, "static")

app = Flask(
	__name__,
	template_folder=template_dir,
	static_folder=static_dir
)

app_settings = os.getenv('APP_SETTINGS', 'project.server.config.DevelopmentConfig')
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from project.server.auth.views import auth_blueprint
app.register_blueprint(auth_blueprint)

from project.server.stickynotes.views import stickynotes_blueprint
app.register_blueprint(stickynotes_blueprint)


@app.route("/")
def login():
	return render_template("login.html")


@app.route("/index")
def index():
	return render_template("index.html")
