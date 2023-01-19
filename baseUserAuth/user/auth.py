from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from baseUserAuth import bcrypt
from baseUserAuth.extensions import db
from baseUserAuth.models import User
from baseUserAuth import mail

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))

    email = request.args.get("email")
    if email:
        return render_template("login.html", email=email)

    email = request.form.get("email")
    password = request.form.get("password")
    remember = request.form.get("remember")

    if email and password:

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            remember = True if remember == "True" else False
            login_user(user, remember=remember)
            print(email, "next", request.args.get("next"))
            return redirect(url_for("home.index"))

        elif user:
            flash("Password was incorrect. Try again", "alert-primary")
            return render_template("login.html", email=email)

        flash("User not found. Please create an acount", "alert-primary")
    print("last", "next", request.args.get("next"))
    return render_template("login.html", email=email)


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if not is_email_unique(email):
            flash("Email already exists. Please log in", "alert-primary")
            return redirect(url_for("auth.login", email=email))

        if not is_username_unique(username):
            flash("Username already exists. Please choose a different username", "alert-primary")
            return render_template("signup.html")

        if password1 != password2:
            flash("Passwords don't match. Try again", "alert-primary")
            return render_template("signup.html", email=email)
        hash_ = bcrypt.generate_password_hash(password1).decode("utf-8")

        new_user = User(email=email, username=username, password=hash_)
        db.session.add(new_user)
        db.session.commit()
        flash("Sign up succesful", "alert-primary")
        return redirect(url_for("auth.login"))

    return render_template("signup.html")


@auth.route("/password_request", methods=["GET", "POST"])
def password_request():
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.get_id()).first()
        token = user.get_reset_token()
        return redirect(url_for("auth.password_reset", token=token))

    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        send_reset_email(user)
        flash(
            "An email has been sent with instructions to reset your password. (Check spam folder)",
            "alert-primary",
        )
        return redirect(url_for("auth.login"))

    return render_template("password_request.html")


@auth.route("/password_reset", methods=["GET", "POST"])
def password_reset():
    token = request.args.get("token")
    print(token)
    if request.method == "POST":
        user = User.verify_reset_token(token)
        if not user:
            flash("That is an invalid or expired token", "alert-primary")

        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if password1 != password2:
            flash("Passwords are not equal. Please try again")
            return render_template("password_reset.html")

        hash_ = bcrypt.generate_password_hash(password1).decode("utf-8")
        user.password = hash_
        db.session.commit()
        flash("Your password has been updated! You are now able to log in", "alert-primary")
        return redirect(url_for("auth.login"))

    return render_template("password_reset.html")


@auth.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = User.query.filter_by(id=current_user.get_id()).first()
    if request.method == "POST":
        username = request.form.get("username")
        if username:
            user.username = username

        email = request.form.get("email")
        if email:
            user.email = email

        db.session.commit()

        return redirect(url_for("auth.profile"))
    return render_template("profile.html", username=user.username, email=user.email)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/username_unique", methods=["GET"])
def username_unique():
    username = request.args.get("username")

    return {"isUnique": is_username_unique(username) }


def is_username_unique(username):
    return not User.query.filter_by(username=username).first()


@auth.route("/email_unique", methods=["GET"])
def email_unique():
    email = request.args.get("email")

    return {"isUnique": is_email_unique(email) }


def is_email_unique(email):
    return not User.query.filter_by(email=email).first()


def send_reset_email(user):
    if not user:
        return

    token = user.get_reset_token()
    msg = Message("Password Reset Request", recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
{url_for('auth.password_reset', token=token, _external=True)}
If you did not make this request then please ignore this email and no changes will be made.
"""
    mail.send(msg)
