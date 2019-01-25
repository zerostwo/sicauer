from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import logout_user, current_user, login_user, login_required
from app import db, bcrypt
from app.users.forms import ResetPasswordForm, RequestResetForm, RegistrationForm, LoginForm, UpdateAccountForm, \
    FaceInfo, ChangeEmailForm
from app.models import User, Post
from app.users.utils import send_reset_email, save_picture, face_info, verification_id, send_email

users = Blueprint('users', __name__, static_folder='static')


@users.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if verification_id(form.student_ID.data, form.password.data) == form.student_ID.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(student_ID=form.student_ID.data, username=form.username.data, email=form.email.data,
                        password=hashed_password)
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            send_email(user.email, '验证你的邮箱', 'email/confirm', user=user, token=token)
            flash('A confirmation email has been sent to you by email.', 'success')
            return redirect(url_for('users.login'))
        else:
            flash('Sign up Unsuccessful. Please check student ID and password.', 'danger')
    return render_template('register.html', title='Register', form=form)


@users.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(student_ID=form.student_ID.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account/', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/confirm/<token>/")
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for("main.home"))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirm your account. Thanks!', 'success')
    else:
        flash('The confirmation link is invalid or has expired', 'danger')
    return redirect(url_for('main.home'))


@users.route('/confirm/')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '确认你的账户', 'email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.', 'success')
    return redirect(url_for('main.home'))


@users.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'users' \
                and request.endpoint != 'static':
            return redirect(url_for('users.unconfirmed'))


@users.route('/unconfirmed/')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.home'))
    return render_template('unconfirmed.html', title='Confirm your account')


@users.route("/reset_password/", methods=['GET', "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>/", methods=['GET', "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('This is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been update! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@users.route('/change_email/', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address', 'email/change_email',
                       user=current_user, token=token)
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template("change_email.html", title="Change email", form=form)


@users.route('/change_email/<token>/', methods=['GET', "POST"])
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Your email address has been updated.', 'success')
        return redirect(url_for('users.account'))
    else:
        flash('Invalid request.', 'danger')
    return redirect(url_for("main.home"))


@users.route("/info/", methods=['GET', 'POST'])
def info():
    form = FaceInfo()
    if form.validate_on_submit():
        a = face_info(user_id=form.user_id.data)
        return render_template('info.html', title='Face', form=form, a=a)
    return render_template('info.html', title='Face', form=form)
