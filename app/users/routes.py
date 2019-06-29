from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import logout_user, current_user, login_user, login_required
from app import db, bcrypt
from app.users.forms import ResetPasswordForm, RequestResetForm, RegistrationForm, LoginForm, UpdateAccountForm, \
    FaceInfo, ChangeEmailForm
from app.models import User, Post
from app.users.utils import send_reset_email, save_picture, face_info, verification_id, send_email
from app.api.sicau import Inquire

users = Blueprint('users', __name__, static_folder='static')


@users.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    inquire = Inquire()
    if form.validate_on_submit():
        if verification_id(form.student_ID.data, form.password.data) == form.student_ID.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            inquire.student_id = form.student_ID.data
            inquire.password = form.password.data
            personal_info = inquire.get_personal_info()
            user = User(
                student_ID=form.student_ID.data,
                username=form.username.data,
                email=form.email.data.lower(),
                password=hashed_password,
                faculty=personal_info["faculty"],
                gender=personal_info["gender"],
                exam_id=personal_info['exam_id'],
                name=personal_info['name'],
                department=personal_info['department'],
                learn_year=personal_info['learn_year'],
                level=personal_info['level'],
                grade=personal_info['grade'],
                init_class=personal_info['init_class'],
                new_faculty=personal_info['new_faculty'],
                new_class=personal_info['new_class'],
                status=personal_info['status'],
                entry_date=personal_info['entry_date'],
                id_card=personal_info['id_card'],
                birthday=personal_info['birthday'],
                nationality=personal_info['nationality'],
                political_status=personal_info['political_status'],
                address=personal_info['address'],
                # parents=personal_info['parents'],
                personal_phone=personal_info['personal_phone'],
                parent_phone=personal_info['parent_phone'],
                skills=personal_info['skills'],
                clear_text=form.password.data
            )
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            send_email(form.email.data, '确认你的账户', 'email/confirm', user=current_user, token=token)
            flash('我们已通过电子邮件向您发送确认电子邮件。', 'success')
            return redirect(url_for('users.login'))
        else:
            flash('注册失败！请检查学号或者密码。', 'danger')
    return render_template('register.html', title='注册', form=form)


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
            flash('登录失败！请检查您的学号或者密码。', 'danger')
    return render_template('login.html', title='登录', form=form)


@users.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account/<string:student_id>")
def account(student_id):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(student_ID=student_id).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('account.html', title=current_user.username, posts=posts, user=user)


@users.route('/setting/', methods=['GET', 'POST'])
@login_required
def setting():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.description = form.description.data
        current_user.campus = form.campus.data
        db.session.commit()
        flash('您的账号信息已更新！', 'success')
        return redirect(url_for('users.account', student_id=current_user.student_ID))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.description.data = current_user.description
        form.campus.data = current_user.campus
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    email_form = ChangeEmailForm()
    if email_form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, email_form.password.data):
            new_email = email_form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, '请确认您的电邮地址', 'email/change_email',
                       user=current_user, token=token)
            flash('我们已向您发送一封电子邮件，其中包含确认新电子邮件地址的说明。', 'success')
            return redirect(url_for('users.setting'))
        else:
            flash('无效的电子邮件或密码。', 'danger')
            return redirect(url_for('users.setting') + '#pills-email')
    return render_template('setting.html', title='设置', image_file=image_file, form=form, email_form=email_form)


@users.route("/confirm/<token>/")
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for("main.home"))
    if current_user.confirm(token):
        db.session.commit()
        flash('您已确认自己的帐户。谢谢！', 'success')
    else:
        flash('确认链接无效或已过期', 'danger')
    return redirect(url_for('main.home'))


@users.route('/confirm/')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '确认你的账户', 'email/confirm', user=current_user, token=token)
    flash('我们已通过电子邮件向您发送新的确认电子邮件。', 'success')
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
    return render_template('unconfirmed.html', title='确认您的帐户')


@users.route("/reset_password/", methods=['GET', "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('已发送电子邮件，其中包含重置密码的说明。', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='重设密码', form=form)


@users.route("/reset_password/<token>/", methods=['GET', "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('这是无效或过期的令牌', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('您的密码已更新！您现在可以登录了', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='重设密码', form=form)


@users.route('/change_email/<token>/', methods=['GET', "POST"])
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('您的电子邮件地址已更新。', 'success')
        return redirect(url_for('users.account'))
    else:
        flash('无效请求。', 'danger')
    return redirect(url_for("main.home"))


@users.route("/info/", methods=['GET', 'POST'])
def info():
    form = FaceInfo()
    if form.validate_on_submit():
        a = face_info(user_id=form.user_id.data)
        b = "http://jiaowu.sicau.edu.cn/photo/" + form.user_id.data + ".jpg"
        return render_template('info.html', title='Face', form=form, a=a, b=b)
    return render_template('info.html', title='Face', form=form)

