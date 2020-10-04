import os

from flask import Flask, redirect, url_for, Blueprint, render_template
from flask_dance.contrib.linkedin import linkedin

from ..utility.linkedin import protected_route

bp = Blueprint('routes', __name__)


@bp.route("/")
@protected_route
def index():
    # if not linkedin.authorized:
    #     return redirect(url_for("linkedin.login"))
    # resp = linkedin.get("me")
    # assert resp.ok
    # data = resp.json()
    # name = "{first} {last}".format(
    #     first=preferred_locale_value(data["firstName"]),
    #     last=preferred_locale_value(data["lastName"]),
    # )
    # resp2 = linkedin.get("emailAddress?q=members&projection=(elements*(handle~))")
    # print(resp2.json())
    # return "You are {name} on LinkedIn".format(name=name)
    return "OK"

@bp.route('/login')
def login():
    return render_template('login.html')
