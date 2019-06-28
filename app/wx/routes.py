from flask import render_template, Blueprint, request
import requests
import json
import hashlib
import time
import xmltodict

wx = Blueprint('wx', __name__)

@wx.route('/wxtest/',methods=['GET','POST'])
def wxtest():
   return "hello"

@wx.route('/wx/',methods=['GET','POST'])
def wechat():
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

