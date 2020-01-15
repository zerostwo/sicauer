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
        Chrome / 71.0.3578.98 Safari / 537.36"}

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
            return BeautifulSoup(data.text, features='lxml')

    def cet(self):
        url = "http://jiaowu.sicau.edu.cn/xuesheng/kao/bao/yycj.asp"
        data1 = {'user': self.student_id, 'pwd': self.password, 'lb': 'S', 'submit': '', 'sign': self.get_sign()}
        post_url = 'http://jiaowu.sicau.edu.cn/jiaoshi/bangong/check.asp'
        self.session.post(post_url, data=data1, timeout=5, headers=self.headers)
        data = {
            "dj": "89321196860502778935097686683832"
        }
        data = self.session.post(url, data=data, timeout=5)
        data.encoding = 'gb2312'
        soup = BeautifulSoup(data.text, features='html5lib')
        r = soup.findAll("td", {"width": "50"})
        return r[6].text

    def cet6(self):
        url = "http://jiaowu.sicau.edu.cn/xuesheng/kao/bao/yycj.asp"
        data1 = {'user': self.student_id, 'pwd': self.password, 'lb': 'S', 'submit': '', 'sign': self.get_sign()}
        post_url = 'http://jiaowu.sicau.edu.cn/jiaoshi/bangong/check.asp'
        self.session.post(post_url, data=data1, timeout=5, headers=self.headers)
        data = {
            "dj": "86041597861062128606986789370776"
        }
        data = self.session.post(url, data=data, timeout=5)
        data.encoding = 'gb289321196860502778935097686683832312'
        soup = BeautifulSoup(data.text, features='html5lib')
        r = soup.findAll("td", {"width": "50"})
        return r[6].text


class Inquire(GetStart):
    def grade(self):
        # 必修课加权平均成绩及专业排名
        url1 = "http://jiaowu.sicau.edu.cn/xuesheng/chengji/chengji/zytongbf.asp"
        soup = self.get_soup(url1)
        #         soup = soup.prettify()
        result = soup.find_all("td", {"align": "left"})
        # 所有课程加权平均成绩及专业排名
        url2 = "http://jiaowu.sicau.edu.cn/xuesheng/chengji/chengji/zytongall.asp"
        soup2 = self.get_soup(url2)
        result2 = soup2.find_all("td", {"align": "left"})
        grade = {
            "bxjq": result[-2].text,
            "bxjq_pm": result[-1].text,
            "sykcjq": result2[-2].text,
            "sykcjq_pm": result2[-1].text
        }
        return grade

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
            "personal_phone": soup_find[20].text,
            "parent_phone": soup_find[21].text,
            "skills": soup_find[22].text,
        }
        return personal_info

    def all(self):
        personal_info = self.get_personal_info()
        grade = self.grade()
        s = ""
        for i in personal_info:
            s += personal_info[i]
            s += "|"
        for j in grade:
            s += grade[j]
            s += "|"
        return s


if __name__ == '__main__':
    info = Inquire()


    def readtxt(file_path):
        l = []
        with open(file_path) as f:
            for i in f.readlines():
                l.append(i.strip())
        return l


    log = open("./info.txt", "a+")
    user_pwd = readtxt("./up.txt")
    for i in user_pwd:
        a = i.split()
        info.student_id = a[0]
        info.password = a[1]
        try:
            r = info.all()
            print(r, file=log)
            print(r)
        except:
            print(info.student_id, "密码错误", file=log)
            print(info.student_id, "密码错误")
