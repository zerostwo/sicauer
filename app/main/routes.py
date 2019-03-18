from flask import render_template, Blueprint, request, jsonify
# from app.models import Post, Comment
import requests
import json

main = Blueprint('main', __name__)


@main.route("/")
# @main.route("/home/")
def home():
    # page = request.args.get('page', 1, type=int)
    # posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    # comments = Comment.query.all()
    # return render_template('index.html', posts=posts, comments=comments)
    return render_template('index.html')


@main.route('/about')
def about():
    return render_template('about.html', title='关于我们')


@main.route('/get_my_ip', methods=['GET'])
def get_my_ip():
    ip = request.headers['X-Forwarded-For']
    # url = f'http://api.ipstack.com/{ip}?access_key=341690b835d7bde8702d3bb6d99e4d3a'
    # r = requests.get(url)
    # j = json.loads(r.text)
    # user_agent = user_agent_parser.Parse(request.headers.get('User-Agent'))
    b = f'http://api.map.baidu.com/location/ip?ip={ip}&ak=fGG3zvzvtNThoWldreWBi3FbKjNxhZbK&coor=bd09ll'
    r = requests.get(b)
    j = json.loads(r.text)
    return jsonify(j), 200
