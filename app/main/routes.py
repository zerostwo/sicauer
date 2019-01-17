from flask import render_template, Blueprint, request
from app.models import Post, User, Comment
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from app import admin, db

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home/")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    comments = Comment.query.all()
    return render_template('index.html', posts=posts, comments=comments)


@main.route('/about/')
def about():
    return render_template('about.html', title='about')


class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

    @expose('/admin/post')
    def post(self):
        return self.render('admin/post.html')


admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Comment, db.session))
