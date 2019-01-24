import requests
from lxml import etree
from bs4 import BeautifulSoup
from requests import exceptions
import re


class GetStart:
    student_id = "201702420"
    password = "981211"
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
           Chrome/71.0.3578.98 Safari/537.36"}

    def get_sign(self):
        index = self.session.get('http://jiaowu.sicau.edu.cn/web/web/web/index.asp', timeout=5)
        index.encoding = 'gb2312'
        return etree.HTML(index.text).xpath("//input[@name='sign']/@value")

    def get_soup(self, url):
        data = {'user': self.student_id, 'pwd': self.password, 'lb': 'S', 'submit': '', 'sign': self.get_sign()}
        try:
            post_url = 'http://jiaowu.sicau.edu.cn/jiaoshi/bangong/check.asp'
            self.session.post(post_url, data=data, timeout=5, headers=self.headers)
        except exceptions.Timeout as e:
            print('请求超时：' + str(e))
        except exceptions.HTTPError as e:
            print('http请求错误:' + str(e))
        else:
            data = self.session.get(url, timeout=5)
            data.encoding = 'gb2312'
            return BeautifulSoup(data.text, features='html5lib')


class Inquire(GetStart):
    def examination_arrangement(self):
        url = 'http://jiaowu.sicau.edu.cn/xuesheng/kao/kao/xuesheng.asp'
        soup = self.get_soup(url)
        subject = soup.find_all('td', {"width": "200"})
        time = soup.find_all('td', {"width": "320"})[1:]
        classroom = soup.find_all('td', {"width": "130"})[1:]
        method = soup.find_all('td', {"width": "80"})[2:]
        seat_number = soup.find_all('td', {"width": "50"})
        seat_number = seat_number[2:]
        examination_arrangement = []
        for i in range(len(subject)):
            intermediate = {
                'num': seat_number[i * 2].string,
                'subject': subject[i].string.strip(),
                'time': time[i].string,
                'classroom': classroom[i].string.strip(),
                'method': method[i].string.strip(),
                'seat_num': seat_number[i * 2 - 1].string.strip()}
            examination_arrangement.append(intermediate)
        return examination_arrangement

    def grade_inquiry(self):
        url = "http://jiaowu.sicau.edu.cn/xuesheng/chengji/chengji/bchengjike.asp"
        soup = self.get_soup(url)
        result_html = soup.find_all('font', {'size': '2'})[20:-3]
        grade = []
        for i in range(int(len(result_html) / 7)):
            intermediate = {
                "num": result_html[i * 7].string,
                "course": result_html[i * 7 + 1].string.strip(),
                "grade": result_html[i * 7 + 2].string.strip(),
                "credit": result_html[i * 7 + 3].string,
                "nature": result_html[i * 7 + 4].string,
                "school_year": result_html[i * 7 + 5].string,
                "semester": result_html[i * 7 + 6].string
            }
            grade.append(intermediate)
        return grade

    def course_info_clear(self, text):
        init = re.findall('(.+?)<br/>', re.findall('width="13.5%">(.+?)</td>', text)[0])
        c = '--------------------'
        if len(init) != 0:
            count = init.count(c)
            p = init.index(c)
            if count != 1:
                for i in init:
                    init[init.index(i)] = re.sub('<(.+?)>', ' ', i)
                course1 = init[:p]
                course2 = init[p + 1:-1]
                course_info = {
                    1: {
                        'course': course1[0],
                        'location': course1[1],
                        'time': course1[2],
                        'experiment': True if len(course1) == 4 else False
                    },
                    2: {
                        'course': course2[0],
                        'location': course2[1],
                        'time': course2[2],
                        'experiment': True if len(course2) == 4 else False
                    }
                }
            else:
                for i in init:
                    init[init.index(i)] = re.sub('<(.+?)>', ' ', i)
                course1 = init[:p]
                course_info = {
                    1: {
                        'course': course1[0],
                        'location': course1[1],
                        'time': course1[2],
                        'experiment': True if len(course1) == 4 else False
                    }
                }
        else:
            course_info = {
                1: {
                    'course': '',
                    'location': '',
                    'time': '',
                    'experiment': ''
                }
            }
        return course_info

    def curriculum(self):
        url = "http://jiaowu.sicau.edu.cn/xuesheng/gongxuan/gongxuan/bxq.asp"
        soup = self.get_soup(url)
        semesters = []
        for semester in soup.find_all('a', {"href": re.compile('xszhinan.asp.*')}):
            semesters.append(semester.string)
        data = {"xueqi": semesters[0]}
        url = "http://jiaowu.sicau.edu.cn/xuesheng/gongxuan/gongxuan/xszhinan.asp"
        select = self.session.post(url, data=data)
        b = self.session.get('http://jiaowu.sicau.edu.cn/xuesheng/gongxuan/gongxuan/kbbanji.asp')
        b.encoding = b.apparent_encoding
        soup2 = BeautifulSoup(b.text, features='html5lib')
        courses = soup2.find_all("td", {"width": "13.5%", "valign": "top", "align": "center", "height": "50"})
        curriculum = {}
        weeks = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i in range(len(weeks)):
            curriculum[weeks[i]] = {
                1: self.course_info_clear(str(courses[0 + i])),
                2: self.course_info_clear(str(courses[7 + i])),
                3: self.course_info_clear(str(courses[14 + i])),
                4: self.course_info_clear(str(courses[21 + i])),
                5: self.course_info_clear(str(courses[28 + i]))
            }
        return curriculum


if __name__ == '__main__':
    inquire = Inquire()
    curriculum = inquire.curriculum()
    mon = []
    for i in range(5):
        mon.append(curriculum['Mon'][i + 1][1]['course'])
    print(mon)
