from flask import Flask
from flask_bcrypt import Bcrypt
from baseUserAuth.config import Config
from baseUserAuth.extensions import db, login_manager
from flask_migrate import Migrate
from flask_mail import Mail

bcrypt = Bcrypt()
migrate = Migrate()
mail = Mail()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "alert-primary"

    mail.init_app(app)

    from baseUserAuth.user.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from baseUserAuth.home.home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    with app.app_context():
        db.create_all()

    migrate.init_app(app, db)

    return app
