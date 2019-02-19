from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    content = TextAreaField('那些现实中不曾发出的声音，请把它留在这里...', validators=[DataRequired()])
    submit = SubmitField('寄存')


class CommentForm(FlaskForm):
    content = StringField('输入您的评论', validators=[DataRequired()])
    submit1 = SubmitField('评论')


class ReplyForm(FlaskForm):
    content = StringField('输入您的回复', validators=[DataRequired()])
    comment_id = IntegerField()
    replied_id = IntegerField()
    submit2 = SubmitField('回复')
