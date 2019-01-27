from flask import render_template, Blueprint, request, jsonify
from app.models import Post, Comment

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home/")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    comments = Comment.query.all()
    return render_template('index.html', posts=posts, comments=comments)


@main.route('/background_process')
def background_process():
    lang = request.args.get('proglang')
    if str(lang).lower() == 'python':
        return jsonify(result='Good')
    else:
        return jsonify(result='Not Good')


@main.route('/about')
def about():
    return render_template('about.html', title='about')
