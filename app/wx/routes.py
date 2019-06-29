from flask import render_template, Blueprint, request, abort
import requests
import hashlib
import time
import xmltodict

wx = Blueprint('wx', __name__)

@wx.route('/wxtest/',methods=['GET','POST'])
def wxtest():
   return "hello"

@wx.route('/wx/',methods=['GET','POST'])
def wechat():
   signature = request.args.get('signature')
   timestamp = request.args.get('timestamp')
   nonce = request.args.get('nonce')
   token = 'duansq'
   list = [token, timestamp, nonce]
   list.sort()
   sha1 = hashlib.sha1()
   sha1.update(list[0].encode('utf-8'))
   sha1.update(list[1].encode('utf-8'))
   sha1.update(list[2].encode('utf-8'))
   hashcode = sha1.hexdigest()
   if hashcode == signature:
      if request.method == "GET":
         echostr = request.args.get('echostr')
         return echostr
      elif request.method == "POST":
         # 微信传输过来的消息
         xml_str = request.data
         if not xml_str:
            abort(400)
         # 对xml字符串进行解析
         xml_dict = xmltodict.parse(xml_str)
         xml_dict = xml_dict.get("xml")
         msg_type = xml_dict.get("MsgType")
         if msg_type == "text":
            # 文本消息
            # 构造返回值。回复给用户的消息
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
                  "Content": "Welcome!"
               }
            }
         resp_xml_str = xmltodict.unparse(resp_dict)
         return resp_xml_str
   else:
      return ""

