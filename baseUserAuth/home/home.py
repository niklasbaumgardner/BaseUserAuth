from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required


home = Blueprint("home", __name__)


@home.route("/", methods=["GET"])
def index():
    return render_template("base.html")