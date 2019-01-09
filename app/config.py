import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.126.com'
    MAIL_PORT = 25
    MAIL_USER_TLS = True
    # MAIL_USERNAME = 'zerostwo@126.com'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = '981211Dd'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
