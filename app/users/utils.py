import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from app import mail
import json
import requests


def save_picture(form_piture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.split(form_piture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_piture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='zerostwo@126.com', recipients=[user.email])
    msg.body = '''To reset your password, visit the following link:
{}
if you did not make this request then simply ignore this email and no change will be made. 
'''.format(url_for('users.reset_token', token=token, _external=True))
    mail.send(msg)


def get_access_token():
    client_id = 'G9yWRpQRxqGLl0vZv2MIqoNE'  # 此变量赋值成自己API Key的值
    client_secret = 'RLol5YGP3EUIEgmQskKLScYvUm3cySvx'  # 此变量赋值成自己Secret Key的值
    auth_url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret

    response_at = requests.get(auth_url)
    json_result = json.loads(response_at.text)
    access_token = json_result['access_token']
    return access_token


def get_info(uid, group_id, url_fi):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    post_data = {
        'uid': uid,
        'user_id': uid,
        'group_id': group_id
    }
    response_fi = requests.post(url_fi, headers=headers, data=post_data)
    json_fi_result = json.loads(response_fi.text)
    return json_fi_result


def face_info(user_id):
    access_token = get_access_token()
    url_fi = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/get?access_token=' + access_token
    id_group = user_id[0:4]
    try:
        json_faces = get_info(user_id, id_group, url_fi)
        return json_faces['result']['user_list'][0]['user_info']
    except:
        return "数据库里面暂时没有收录人脸。"
