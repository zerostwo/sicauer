from flask import Blueprint
from app.models import Post, User, Comment, Reply
from flask_admin.contrib.sqla import ModelView
from app import admin, db

super_admin = Blueprint('super_admin', __name__)

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Comment, db.session))
admin.add_view(ModelView(Reply, db.session))
