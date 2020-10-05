import os

from flask import Flask, redirect, url_for, Blueprint, render_template
from flask_dance.contrib.linkedin import linkedin

from ..utility.linkedin import protected_route

bp = Blueprint('routes', __name__)


@bp.route("/")
@protected_route
def index():
    return render_template('index.html')

@bp.route('/login')
def login():
    return render_template('login.html')
