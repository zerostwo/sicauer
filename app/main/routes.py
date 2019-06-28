from flask import render_template, Blueprint, request, jsonify, abort
# from app.models import Post, Comment
import requests
import json
import hashlib
import time
import xmltodict

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

@main.route('/wx/',methods=['GET','POST'])
def wx():
   if request.method == "GET":
      signature = request.args.get('signature')
      timestamp = request.args.get('timestamp')
      nonce = request.args.get('nonce')
      echostr = request.args.get('echostr')
      token = 'duansq'
      list = [token, timestamp, nonce]
      list.sort()
      sha1 = hashlib.sha1()
      sha1.update(list[0].encode('utf-8'))
      sha1.update(list[1].encode('utf-8'))
      sha1.update(list[2].encode('utf-8'))
      hashcode = sha1.hexdigest()
      if hashcode == signature:
         return echostr
      else:
         return ""

   elif request.method == "POST":
      xml_str = request.data
      if not xml_str:
         abort(400)
# return xml_str
      xml_dict = xmltodict.parse(xml_str)
      xml_dict = xml_dict.get("xml")
      msg_type = xml_dict.get("MsgType")
      if msg_type == "text":
         resp_dict = {
            "xml": {
               "ToUserName": xml_dict.get("FromUserName"),
               "FromUserName": xml_dict.get("ToUserName"),
               "CreateTime": int(time.time()),
               "MsgType": "text",
               "Content": xml_dict.get("Content")
            }
         }
      else:
         resp_dict = {
                    "xml": {
                        "ToUserName": xml_dict.get("FromUserName"),
                        "FromUserName": xml_dict.get("ToUserName"),
                        "CreateTime": int(time.time()),
                        "MsgType": "text",
                        "Content": "欢迎来的薛定谔的杂货铺，目前正在装修店面..."
                    }
                }
            # 将字典转换为xml字符串
      resp_xml_str = xmltodict.unparse(resp_dict)
            # 返回消息数据给微信服务器
      return resp_xml_str

