from flask import render_template, Blueprint, request, jsonify, abort, url_for
# from app.models import Post, Comment
import requests
import json
import os
import random

main = Blueprint('main', __name__)


@main.route("/bqb")
# @main.route("/home/")
def bqb():
    # page = request.args.get('page', 1, type=int)
    # posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    # comments = Comment.query.all()
    # return render_template('index.html', posts=posts, comments=comments)
    return render_template('bqb.html')


@main.route('/about')
def about():
    return render_template('about.html', title='关于我们')

@main.route('/apple')
def apple():
    return render_template('email/apple.html', title='关于我们')

@main.route('/postman')
def postman():
    return render_template('email/postman.html', title='关于我们')

@main.route('/sendgrid')
def sendgrid():
    return render_template('email/sendgrid.html', title='关于我们')

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

#@main.route('/bqb', methods=['GET'])
@main.route("/")
def home():
   images = os.listdir("app/static/bqb")
   random_image = random.choice(images)
   image_path = "static/bqb/" + random_image
   image_name = random_image[:-4]
   return render_template('index.html', image_path=image_path, image_name=image_name)
@main.route("/one")
def one():
   images = os.listdir("app/static/one")
   random_image = random.choice(images)
   image_path = "static/one/" + random_image
   image_name = random_image[:-4]
   return render_template('one.html', image_path=image_path, image_name=image_name)

@main.route("/video", methods=["GET"])
def video():
   videos = os.listdir("app/static/videos/")
   return render_template('videos.html', videos=videos)
