from app import db, login_manager
from datetime import datetime
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from werkzeug.security import check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    student_ID = db.Column(db.String(10), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    clear_text = db.Column(db.String(20))
    image_file = db.Column(db.String(120), nullable=False, default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    confirmed = db.Column(db.Boolean, default=False)
    member_since = db.Column(db.DateTime(), default=datetime.now)
    last_seen = db.Column(db.DateTime(), default=datetime.now)
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    replies = db.relationship('Reply', backref='author', lazy='dynamic')
    campus = db.Column(db.String(20))
    description = db.Column(db.String(240))
    domain = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    faculty = db.Column(db.String(120))
    exam_id = db.Column(db.String(20))
    name = db.Column(db.String(20))
    department = db.Column(db.String(20))
    learn_year = db.Column(db.String(20))
    level = db.Column(db.String(20))
    grade = db.Column(db.String(20))
    init_class = db.Column(db.String(20))
    new_faculty = db.Column(db.String(20))
    new_class = db.Column(db.String(20))
    status = db.Column(db.String(20))
    entry_date = db.Column(db.String(20))
    id_card = db.Column(db.String(20))
    birthday = db.Column(db.String(20))
    nationality = db.Column(db.String(20))
    political_status = db.Column(db.String(20))
    address = db.Column(db.String(120))
    parents = db.Column(db.String(20))
    personal_phone = db.Column(db.String(20))
    parent_phone = db.Column(db.String(20))
    skills = db.Column(db.String(20))

    def ping(self):
        self.last_seen = datetime.now()
        db.session.add(self)
        db.session.commit()

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def generate_email_change_token(self, new_email, expiration=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def __repr__(self):
        return f"{self.username}"


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def __repr__(self):
        return f"{self.content}"


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    date_posted = db.Column(db.DateTime, index=True, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.Text)
    replies = db.relationship('Reply', backref='comment', lazy='dynamic')

    def __repr__(self):
        return f"{self.content}"


class Reply(db.Model):
    __tablename__ = 'replies'
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    date_posted = db.Column(db.DateTime, index=True, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.Text)
    replied_id = db.Column(db.Integer, db.ForeignKey('replies.id'))  # parent id
    replies_z = db.relationship('Reply', back_populates='replied', cascade='all, delete-orphan')
    replied = db.relationship('Reply', back_populates='replies_z', remote_side=[id])  # child_id

    def __repr__(self):
        return f"{self.content}"
