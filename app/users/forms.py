from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField, DateField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from flask_login import current_user
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    student_ID = StringField('Student ID', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    student_ID = StringField('Student ID', validators=[DataRequired()])
    # email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'png', 'JPEG', 'JPG', 'PNG', 'jpeg'])])
    gender = SelectField('Gender', choices=[('', '选择您的性别...'), ('male', '男'), ('female', '女')])
    birthday = DateField('Birthday', format='%m/%d/%Y', validators=[Optional()])
    campus = SelectField('Campus',
                         choices=[('', '选择您所在的校区...'), ('成都校区', '成都校区'), ('都江堰校区', '都江堰校区'), ('雅安校区', '雅安校区')],
                         default='')
    faculty = SelectField('Faculty',
                          choices=[('', '选择您的专业...'), ('经济学 ', '经济学 '), ('金融学 ', '金融学 '), ('投资学 ', '投资学 '),
                                   ('国际经济与贸易 ', '国际经济与贸易 '),
                                   ('法学 ', '法学 '), ('政治学与行政学 ', '政治学与行政学 '), ('社会工作 ', '社会工作 '), ('教育技术学 ', '教育技术学 '),
                                   ('体育教育 ', '体育教育 '), ('社会体育指导与管理 ', '社会体育指导与管理 '), ('休闲体育 ', '休闲体育 '),
                                   ('汉语言文学 ', '汉语言文学 '), ('英语 ', '英语 '), ('广告学 ', '广告学 '), ('信息与计算科学 ', '信息与计算科学 '),
                                   ('应用物理学 ', '应用物理学 '), ('应用化学 ', '应用化学 '), ('化学生物学 ', '化学生物学 '),
                                   ('自然地理与资源环境 ', '自然地理与资源环境 '), ('人文地理与城乡规划 ', '人文地理与城乡规划 '), ('地理信息科学 ', '地理信息科学 '),
                                   ('生物科学 ', '生物科学 '), ('生物技术 ', '生物技术 '), ('生态学 ', '生态学 '), ('能源与动力工程 ', '能源与动力工程 '),
                                   ('电气工程及其自动化 ', '电气工程及其自动化 '), ('电子科学与技术 ', '电子科学与技术 '), ('计算机科学与技术 ', '计算机科学与技术 '),
                                   ('物联网工程 ', '物联网工程 '), ('土木工程 ', '土木工程 '), ('给排水科学与工程 ', '给排水科学与工程 '),
                                   ('道路桥梁与渡河工程 ', '道路桥梁与渡河工程 '), ('水利水电工程 ', '水利水电工程 '), ('包装工程 ', '包装工程 '),
                                   ('农业机械化及其自动化 ', '农业机械化及其自动化 '), ('农业水利工程 ', '农业水利工程 '), ('木材科学与工程 ', '木材科学与工程 '),
                                   ('环境工程 ', '环境工程 '), ('环境科学 ', '环境科学 '), ('环境生态工程 ', '环境生态工程 '),
                                   ('食品科学与工程 ', '食品科学与工程 '), ('食品质量与安全 ', '食品质量与安全 '), ('建筑学 ', '建筑学 '),
                                   ('城乡规划 ', '城乡规划 '), ('风景园林 ', '风景园林 '), ('生物工程 ', '生物工程 '), ('农学 ', '农学 '),
                                   ('园艺 ', '园艺 '), ('植物保护 ', '植物保护 '), ('植物科学与技术 ', '植物科学与技术 '),
                                   ('种子科学与工程 ', '种子科学与工程 '), ('设施农业科学与工程 ', '设施农业科学与工程 '), ('茶学 ', '茶学 '),
                                   ('烟草 ', '烟草 '), ('农业资源与环境 ', '农业资源与环境 '), ('野生动物与自然保护区管理 ', '野生动物与自然保护区管理 '),
                                   ('水土保持与荒漠化防治 ', '水土保持与荒漠化防治 '), ('动物科学 ', '动物科学 '), ('动物医学 ', '动物医学 '),
                                   ('动植物检疫 ', '动植物检疫 '), ('林学 ', '林学 '), ('园林 ', '园林 '), ('森林保护 ', '森林保护 '),
                                   ('水产养殖学 ', '水产养殖学 '), ('草业科学 ', '草业科学 '), ('药学 ', '药学 '), ('药物制剂 ', '药物制剂 '),
                                   ('中草药栽培与鉴定 ', '中草药栽培与鉴定 '), ('信息管理与信息系统 ', '信息管理与信息系统 '), ('工程管理 ', '工程管理 '),
                                   ('工程造价 ', '工程造价 '), ('工商管理 ', '工商管理 '), ('市场营销 ', '市场营销 '), ('会计学 ', '会计学 '),
                                   ('财务管理 ', '财务管理 '), ('人力资源管理 ', '人力资源管理 '), ('审计学 ', '审计学 '), ('资产评估 ', '资产评估 '),
                                   ('文化产业管理 ', '文化产业管理 '), ('农林经济管理 ', '农林经济管理 '), ('农村区域发展 ', '农村区域发展 '),
                                   ('行政管理 ', '行政管理 '), ('土地资源管理 ', '土地资源管理 '), ('电子商务 ', '电子商务 '), ('旅游管理 ', '旅游管理 '),
                                   ('酒店管理 ', '酒店管理 '), ('会展经济与管理 ', '会展经济与管理 '), ('视觉传达设计 ', '视觉传达设计 '),
                                   ('环境设计 ', '环境设计 '), ('产品设计 ', '产品设计 '), ('数字媒体艺术 ', '数字媒体艺术 ')]
                          )
    description = TextAreaField('Description')
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Passworf Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Email already registered.')


class FaceInfo(FlaskForm):
    user_id = StringField('学号', validators=[DataRequired()])
    submit = SubmitField('查询')
