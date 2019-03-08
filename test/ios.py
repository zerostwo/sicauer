import requests
from lxml import etree
import datetime as d
from bs4 import BeautifulSoup


def student_name(student_id, pwd):
    session = requests.Session()
    t = d.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        index = session.get('http://jiaowu.sicau.edu.cn/web/web/web/index.asp', timeout=5)
        index.encoding = 'gb2312'
        seletor = etree.HTML(index.text)
        sign = seletor.xpath("//input[@name='sign']/@value")
        data = {'user': student_id, 'pwd': pwd, 'lb': 'S', 'submit': '', 'sign': sign}
        try:
            post_url = 'http://jiaowu.sicau.edu.cn/jiaoshi/bangong/check.asp'
            try:
                session.post(post_url, data=data, timeout=5)
                data = session.get('http://jiaowu.sicau.edu.cn/xuesheng/cx/zhcp/bzr_zhcj.asp', timeout=5)
            except:
                print(student_id, pwd, 'Connection_timed_out_2')
            data.encoding = 'gb2312'
            soup = BeautifulSoup(data.text)
            nameAndId = soup.find_all('td', {"class": "g_body"})
            #             for i in range(int(len(nameAndId))):
            #                 print(nameAndId[i*3+4].string, nameAndId[i*3+5].string)
            return nameAndId, len(nameAndId)
        except:
            print(student_id, pwd, 'wrong_password', t)
    except:
        print(student_id, pwd, 'Connection_timed_out_1', t)


if __name__ == '__main__':
    print(student_name(201702420, 981211))
