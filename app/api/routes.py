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


@api.route("/curriculum/")
def curriculum_info():
    inquire = Inquire()
    curriculum = inquire.curriculum()
    mon = []
    for i in range(5):
        mon.append(curriculum['Mon'][i + 1][1]['course'])
    tue = []
    for i in range(5):
        tue.append(curriculum['Tue'][i + 1][1]['course'])
    wed = []
    for i in range(5):
        wed.append(curriculum['Wed'][i + 1][1]['course'])
    thu = []
    for i in range(5):
        thu.append(curriculum['Thu'][i + 1][1]['course'])
    fri = []
    for i in range(5):
        fri.append(curriculum['Fri'][i + 1][1]['course'])
    sat = []
    for i in range(5):
        sat.append(curriculum['Sat'][i + 1][1]['course'])
    sun = []
    for i in range(5):
        sun.append(curriculum['Sun'][i + 1][1]['course'])
    return render_template('curriculum.html',
                           mon=mon,
                           tue=tue,
                           wed=wed,
                           thu=thu,
                           fri=fri,
                           sat=sat,
                           sun=sun
                           )
