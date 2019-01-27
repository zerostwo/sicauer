from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    content = StringField('Enter your comment', validators=[DataRequired()])
    submit1 = SubmitField('Comment')


class ReplyForm(FlaskForm):
    content = StringField('Enter your reply', validators=[DataRequired()])
    comment_id = IntegerField()
    replied_id = IntegerField()
    submit2 = SubmitField('Reply')
