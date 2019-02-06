from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from app import db
from app.models import Post, Comment, Reply
from app.posts.forms import PostForm, CommentForm, ReplyForm
import os

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('您的秘密已经寄存！', 'success')
        return redirect(url_for('main.home'))
    # if request.method == 'POST':
    # f = request.files.get('file')
    # f.save(os.path.join(url_for('static', filename='uploads'), f.filename))
    return render_template('create_post.html', title='树洞', form=form, legend="树洞")


@posts.route('/post/<int:post_id>/', methods=['GET', 'POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.submit1.data and form.validate_on_submit():
        comment = Comment(content=form.content.data, post=post, author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('您的评论已发布。', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    reply_form = ReplyForm()
    if reply_form.submit2.data and reply_form.validate_on_submit():
        reply = Reply(content=reply_form.content.data, comment_id=reply_form.comment_id.data,
                      replied_id=reply_form.replied_id.data,
                      author=current_user._get_current_object())
        db.session.add(reply)
        db.session.commit()
        flash('您的回复已发布。', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    comments = Comment.query.order_by(Comment.date_posted.desc()).filter_by(post_id=post.id).all()
    replies = Reply.query.all()
    return render_template('post.html', title='详情', post=post, form=form, comments=comments, replies=replies,
                           reply_form=reply_form)


@posts.route("/post/<int:post_id>/update/", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.content = form.content.data
        db.session.commit()
        flash('您的帖子已更新！', 'success')
        return redirect(url_for('.post', post_id=post.id))
    elif request.method == 'GET':
        form.content.data = post.content
    return render_template('create_post.html', title='更新帖子', form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete/", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('您的帖子已被删除！', 'success')
    return redirect(url_for('main.home'))
