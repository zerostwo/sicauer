from flask import Blueprint
from flask_admin.menu import MenuLink
from datetime import date
from flask_admin.model import typefmt
from app.models import Post, User, Comment, Reply
from flask_admin.contrib.sqla import ModelView
from app import admin, db

super_admin = Blueprint('super_admin', __name__)


def date_format(view, value):
    return value.strftime('%Y/%m/%d %H:%M:%S')


MY_DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
MY_DEFAULT_FORMATTERS.update({
    type(None): typefmt.null_formatter,
    date: date_format
})


class UserView(ModelView):
    can_view_details = True
    column_exclude_list = ['password', ]
    column_searchable_list = ['student_ID', 'username', 'email']
    column_filters = ['confirmed']
    column_editable_list = ['username', 'email', 'confirmed']
    form_excluded_columns = ['posts', 'comments', 'replies', 'last_seen']
    can_export = True
    column_type_formatters = MY_DEFAULT_FORMATTERS
    column_sortable_list = ('student_ID', 'last_seen', 'member_since')
    column_labels = {
        'member_since': 'Since',
        'image_file': 'Avatar'
    }


class PostView(ModelView):
    form_excluded_columns = ['comments']
    column_editable_list = ['content']
    column_searchable_list = ['content', 'author.username']
    column_type_formatters = MY_DEFAULT_FORMATTERS


class CommentView(ModelView):
    form_excluded_columns = ['replies']
    column_editable_list = ['content']
    column_searchable_list = ['content', 'author.username']
    column_type_formatters = MY_DEFAULT_FORMATTERS


class ReplyView(ModelView):
    form_excluded_columns = ['replies_z']
    column_editable_list = ['content']
    column_searchable_list = ['content', 'author.username']
    column_type_formatters = MY_DEFAULT_FORMATTERS


admin.add_view(UserView(User, db.session))
admin.add_view(PostView(Post, db.session))
admin.add_view(CommentView(Comment, db.session))
admin.add_view(ReplyView(Reply, db.session))
admin.add_link(MenuLink(name='Home Page', url='/'))
