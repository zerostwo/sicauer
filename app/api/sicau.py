import requests
from lxml import etree
from bs4 import BeautifulSoup
from requests import exceptions


class GetStart:
    student_id = "201702442"
    password = "123123"
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

    def course_selection_or_withdrawal(self):
        url = "http://jiaowu.sicau.edu.cn/xuesheng/gongxuan/gongxuan/bxq.asp"
        soup = self.get_soup(url)
        return soup.prettify()
