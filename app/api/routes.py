from flask import Blueprint, render_template
from app.api.sicau import Inquire

api = Blueprint('api', __name__)


@api.route("/grade")
def grade():
    inquire = Inquire()
    grades = inquire.grade_inquiry()
    return render_template('grade.html', grades=grades)
