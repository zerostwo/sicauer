import requests
from lxml import etree
from bs4 import BeautifulSoup


def personnal_info(student_id, password):
    session = requests.Session()
    index = session.get('http://jiaowu.sicau.edu.cn/web/web/web/index.asp', timeout=5)
    index.encoding = 'gb2312'
    selector = etree.HTML(index.text)
    sign = selector.xpath("//input[@name='sign']/@value")
    data = {
        'user': student_id,
        'pwd': password,
        'lb': 'S',
        'submit': '',
        'sign': sign
    }
    post_url = 'http://jiaowu.sicau.edu.cn/jiaoshi/bangong/check.asp'
    session.post(post_url, data=data, timeout=5)
    personal_info = session.get('http://jiaowu.sicau.edu.cn/xuesheng/dangan/banji/bjiben.asp', timeout=5)
    personal_info.encoding = 'gb2312'
    soup = BeautifulSoup(personal_info.text, features="lxml")
    d = soup.find_all('a', {'class': "g_body"})
    info = d[0:6] + d[8:19] + d[21:23]
    for i in info:
        print(i.get_text())


def class_info(student_id, password):
    session = requests.Session()
    index = session.get('http://jiaowu.sicau.edu.cn/web/web/web/index.asp', timeout=5)
    index.encoding = 'gb2312'
    selector = etree.HTML(index.text)
    sign = selector.xpath("//input[@name='sign']/@value")
    data = {
        'user': student_id,
        'pwd': password,
        'lb': 'S',
        'submit': '',
        'sign': sign
    }
    post_url = 'http://jiaowu.sicau.edu.cn/jiaoshi/bangong/check.asp'
    session.post(post_url, data=data, timeout=5)
    class_info = session.get('http://jiaowu.sicau.edu.cn/xuesheng/cx/zhcp/bzr_zhcj.asp', timeout=5)
    class_info.encoding = 'gb2312'
    soup = BeautifulSoup(class_info.text, features="lxml")
    d = soup.find_all('td', {'class': "g_body"})
    s = []
    for i in range(int(len(d)) // 9):
        s = d[0 + i * 9:1 + i * 9] + d[2 + i * 9:6 + i * 9]
        print(s[0].get_text(), s[1].get_text(), s[2].get_text(), s[3].get_text())


def score_info(student_id, password):
    session = requests.Session()
    index = session.get('http://jiaowu.sicau.edu.cn/web/web/web/index.asp', timeout=5)
    index.encoding = 'gb2312'
    selector = etree.HTML(index.text)
    sign = selector.xpath("//input[@name='sign']/@value")
    data = {
        'user': student_id,
        'pwd': password,
        'lb': 'S',
        'submit': '',
        'sign': sign
    }
    post_url = 'http://jiaowu.sicau.edu.cn/jiaoshi/bangong/check.asp'
    session.post(post_url, data=data, timeout=5)
    score_info = session.get('http://jiaowu.sicau.edu.cn/xuesheng/chengji/chengji/bchengjike.asp', timeout=5)
    score_info.encoding = 'gb2312'
    soup = BeautifulSoup(score_info.text, features="lxml")
    course = soup.find_all('td', {"width": "20%"})
    score = soup.find_all('td', {"width": "5%"})
    for i in score:
        print(i.get_text())


a = ''
b = ''
score_info(a, b)
