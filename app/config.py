class Config:
    SECRET_KEY = 'aea9c1ddec6a9e7db162b41afbff9a6d'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.126.com'
    MAIL_PORT = 25
    MAIL_USER_TLS = True
    MAIL_USERNAME = 'zerostwo@126.com'
    # app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = '981211Dd'
    # app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
