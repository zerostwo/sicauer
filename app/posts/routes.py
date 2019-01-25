from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from app import db
from app.models import Post, Comment
from app.posts.forms import PostForm, CommentForm
import shortuuid
from datetime import datetime

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend="New Post")


@posts.route('/post/<int:post_id>/', methods=['GET', 'POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, post=post, author=current_user._get_current_object(),
                          reply_id=shortuuid.uuid())
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    comments = Comment.query.order_by(Comment.date_posted.desc()).filter_by(post_id=post.id).all()
    return render_template('post.html', title='More', post=post, form=form, comments=comments)


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
        flash('Your post has been updated!', 'success')
        return redirect(url_for('.post', post_id=post.id))
    elif request.method == 'GET':
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete/", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
