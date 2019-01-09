import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from app import app, mail


def save_picture(form_piture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.split(form_piture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
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
