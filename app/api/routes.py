from flask import Blueprint, render_template, jsonify
from app.api.sicau import Inquire
from flask_login import current_user

api = Blueprint('api', __name__)


@api.route("/grade")
def grade():
    inquire = Inquire()
    inquire.student_id = current_user.student_ID
    inquire.password = current_user.clear_text
    grade_info = inquire.grade()
    grades = grade_info[0]
    one = grade_info[1]
    subjects = list(one.keys())[:-1]
    scores = list(one.values())[:-1]
    w1 = list(one.keys())[-1]
    w2 = list(one.values())[-1]
    credit = inquire.credit()
    a = credit[0]
    b = credit[1]
    return render_template('grade.html', grades=grades, one=one, subjects=subjects, scores=scores, w1=w1, w2=w2, a=a,
                           b=b, title='成绩信息')


@api.route("/personal_info")
def personal_info():
    inquire = Inquire()
    inquire.student_id = current_user.student_ID
    inquire.password = current_user.clear_text
    return jsonify(inquire.get_personal_info())


@api.route("/isicau")
def isicau():
    inquire = Inquire()
    getUserSchoolActList = inquire.isicau()
    return jsonify(getUserSchoolActList)


@api.route("/curriculum/")
def curriculum_info():
    inquire = Inquire()
    curriculum = inquire.curriculum()
    a0 = []
    for i in curriculum[0]:
        a0.append(i[1]['course'])
    a1 = []
    for i in curriculum[1]:
        a1.append(i[1]['course'])
    a2 = []
    for i in curriculum[2]:
        a2.append(i[1]['course'])
    a3 = []
    for i in curriculum[3]:
        a3.append(i[1]['course'])
    a4 = []
    for i in curriculum[4]:
        a4.append(i[1]['course'])

    # return jsonify(curriculum)
    return render_template('curriculum.html', a0=a0, a1=a1, a2=a2, a3=a3, a4=a4)
