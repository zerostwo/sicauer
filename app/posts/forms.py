from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    content = StringField('Enter your comment', validators=[DataRequired()])
    submit = SubmitField('Comment')


class ReplyForm(FlaskForm):
    content = StringField('Enter your reply', validators=[DataRequired()])
    submit = SubmitField('Reply')
