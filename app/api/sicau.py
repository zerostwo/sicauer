import re

import requests
from bs4 import BeautifulSoup
from lxml import etree
from requests import exceptions


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

    def grade(self):
        url = "http://jiaowu.sicau.edu.cn/xuesheng/chengji/chengji/bchengjike.asp"
        soup = self.get_soup(url)
        result_html = soup.find_all('font', {'size': '2'})[20:-3]
        grade = []
        school_year = []
        for i in range(int(len(result_html) / 7)):
            intermediate = {
                "num": result_html[i * 7].string,
                "course": result_html[i * 7 + 1].string.strip(),
                "grade": result_html[i * 7 + 2].text.strip(),
                "credit": result_html[i * 7 + 3].string,
                "nature": result_html[i * 7 + 4].string,
                "school_year": result_html[i * 7 + 5].string,
                "semester": result_html[i * 7 + 6].string
            }
            if result_html[i * 7 + 5].string not in school_year:
                school_year.append(result_html[i * 7 + 5].string)
            grade.append(intermediate)
        one = {}
        all_a = 0
        all_b = 0
        for j in school_year:
            for k in ['1', '2']:
                a = 0
                b = 0
                for i in grade:
                    if i['semester'] == k and i['school_year'] == j and i['nature'] == '必修':
                        all_a += float(i['credit']) * float(i['grade'])
                        a += float(i['credit']) * float(i['grade'])
                        all_b += float(i['credit'])
                        b += float(i['credit'])
                if b != 0:
                    one[f'{j}-{k}'] = round(a / b, 2)
                else:
                    one['compulsory_weighting'] = round(all_a / all_b, 2)
        return [grade, one]

    def credit(self):
        url = 'http://jiaowu.sicau.edu.cn/xuesheng/chengji/xdjd/xuefen.asp'
        soup = self.get_soup(url)
        # soup_find = soup.find_all('td', {'align': 'center', 'valign': "middle"})
        soup_find = soup.find_all('div', {'align': 'center'})
        a = []
        for i in soup_find:
            if i.text.strip() != '':
                a.append(i.text.strip())
        return [a[-3], a[-4]]

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
        # curriculum = {}
        # weeks = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        # for i in range(len(weeks)):
        #     curriculum[weeks[i]] = {
        #         1: self.course_info_clear(str(courses[0 + i])),
        #         2: self.course_info_clear(str(courses[7 + i])),
        #         3: self.course_info_clear(str(courses[14 + i])),
        #         4: self.course_info_clear(str(courses[21 + i])),
        #         5: self.course_info_clear(str(courses[28 + i]))
        #     }
        curriculum = {}
        for i in range(6):
            curriculum[i] = {

            }
        return courses

    def faculty(self):
        url = "http://jiaowu.sicau.edu.cn/web/web/web/profession.htm"
        soup = self.get_soup(url)
        soup_find = soup.find_all('td', {'class': 'xl66'})
        subjects_info = []
        for i in range(int(len(soup_find) / 5)):
            subject_info = {
                "id": soup_find[i * 5].text,
                "name": soup_find[1 + i * 5].text,
                "year": soup_find[2 + i * 5].text,
                "category": soup_find[3 + i * 5].text,
                "faculty": soup_find[4 + i * 5].text
            }
            subjects_info.append(subject_info)
        return subjects_info

    def get_personal_info(self):
        url = "http://jiaowu.sicau.edu.cn/xuesheng/dangan/banji/bjiben.asp"
        soup = self.get_soup(url)
        soup_find = soup.find_all("a", {"class": "g_body"})
        personal_info = {
            "exam_id": soup_find[0].text,
            "student_id": soup_find[1].text,
            "name": soup_find[2].text,
            "gender": soup_find[3].text,
            "department": soup_find[4].text,
            "faculty": soup_find[5].text,
            "learn_year": soup_find[6].text,
            "level": soup_find[7].text,
            "grade": soup_find[8].text,
            "init_class": soup_find[9].text,
            "new_faculty": soup_find[10].text,
            "new_class": soup_find[11].text,
            "status": soup_find[12].text,
            "entry_date": soup_find[13].text,
            "id_card": soup_find[14].text,
            "birthday": soup_find[15].text,
            "nationality": soup_find[16].text,
            "political_status": soup_find[17].text,
            "address": soup_find[18].text,
            "parents": soup_find[20].text,
            "personal_phone": soup_find[21].text,
            "parent_phone": soup_find[22].text,
            "skills": soup_find[23].text,
        }
        return personal_info


if __name__ == '__main__':
    inquire = Inquire()
    print(inquire.curriculum())

