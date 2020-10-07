from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_dance.contrib.linkedin import make_linkedin_blueprint, linkedin


app = Flask(__name__)
app.config.from_pyfile('settings.py')

# sql connection
sqldb = SQLAlchemy(app)

# ensure all tables
migrate = Migrate(app, sqldb)

# linkedin login
linkedin_bp = make_linkedin_blueprint(scope=["r_liteprofile", "r_emailaddress"])
app.register_blueprint(linkedin_bp, url_prefix="/login")

# repositories
from .db.repository.UserRepository import UserRepository
user_repository = UserRepository()

# register the routes
from .routes.routes import bp
app.register_blueprint(bp)

# import db models for migrations
from .db import models

import flask_whooshalchemy
@app.before_first_request
def initiate_index():
    flask_whooshalchemy.search_index(app, models.Clause)