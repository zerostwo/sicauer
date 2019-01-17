import requests
from lxml import etree
import re


def verification_id(student_id, password):
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
    try:
        post_url = 'http://jiaowu.sicau.edu.cn/jiaoshi/bangong/check.asp'
        session.post(post_url, data=data, timeout=5)
        data = session.get('http://jiaowu.sicau.edu.cn/xuesheng/bangong/main/index1.asp', timeout=5)
        data.encoding = 'gb2312'
        info = re.compile('<td width="99" align="left">(.*)</td>').findall(data.text)
        return info[0]
    except:
        return False


student_id = '201702420'
password = '981211'
print(verification_id(student_id, password))
