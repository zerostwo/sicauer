from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_mail import Mail
from app.config import Config
from flask_admin import Admin, AdminIndexView
from flask_moment import Moment

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
moment = Moment()
admin = Admin(name="Sicauer", template_mode='bootstrap3')


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.student_ID == '201702420':
            return True
        return False


def create_app(config_class=Config):
    app = Flask(__name__)
    from app.models import User
    from app.models import Post
    from app.models import Comment
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    admin.init_app(app, index_view=MyAdminIndexView())
    moment.init_app(app)
    from app.users.routes import users
    from app.posts.routes import posts
    from app.main.routes import main
    from app.errors.handlers import errors
    from app.books.routes import books
    from app.api.routes import api
    app.register_blueprint(users)
    app.register_blueprint(books)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(api)

    return app
