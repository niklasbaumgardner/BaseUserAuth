from baseUserAuth.models import User
from baseUserAuth.extensions import db
from baseUserAuth import bcrypt


def createUser(email, username, password):
    hash_ = hashPassword(password=password)
    new_user = User(email=email, username=username, password=hash_)
    db.session.add(new_user)
    db.session.commit()


def getUserById(id):
    return User.query.filter_by(id=id).first()


def getUserByEmail(email):
    return User.query.filter_by(email=email).first()


def updateUser(id, username, email):
    user = getUserById(id=id)

    if username:
        user.username = username

    if email:
        user.email = email

    db.session.commit()


def updateUserPasswod(id, password):
    if not password or not id:
        return

    user = getUserById(id=id)
    hash_ = hashPassword(password=password)
    user.password = hash_

    db.session.commit()


def hashPassword(password):
    return bcrypt.generate_password_has(password=password).decode("uft-8")


def is_email_unique(email):
    return not User.query.filter_by(email=email).first()


def is_username_unique(username):
    return not User.query.filter_by(username=username).first()