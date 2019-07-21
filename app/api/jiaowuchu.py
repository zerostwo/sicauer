# Date: Sun May 19 10:42:28 CST 2019
# Author: duansq
# https://api.sicauer.com/v1/jiaowuchu/
# url: http://jiaowu.sicau.edu.cn

import requests
from bs4 import BeautifulSoup
import re


class Jiaowuchu:
    studentID = "201702420"
    password = "981211"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/71.0.3578.98 Safari/537.36",
        'Referer': 'http://jiaowu.sicau.edu.cn/web/web/web/index.asp',
        "Host": "jiaowu.sicau.edu.cn",
        "Accept": "text/html,applicationxhtml+xml,application/xml;q=0.9,image/webp,image/apng,\
            */*;q=0.8,application/signed-exchange;v=b3",
    }
    session = requests.Session()
    session.get("http://jiaowu.sicau.edu.cn/web/web/web/index.asp")

    def getSoup(self, url):
        """
        获取网页内容并且转化为Beatifulsoup对象
        :param url: 域名
        :return: Beatifulsoup对象
        """
        r = self.session.get(url)
        r.encoding = 'gb2312'
        return BeautifulSoup(r.text, features='html5lib')
        # return BeautifulSoup(r.text, features='lxml')

    def signValue(self):
        """
        获取登陆教务网时必须参数sign的value
        :return: value值
        """
        url = 'http://jiaowu.sicau.edu.cn/web/web/web/index.asp'
        return self.getSoup(url).find("input", {"name": "sign"})['value']

    def getUrl(self, url):
        """
        获取url下的所有超链接
        :param url: 域名
        :return: 域名列表
        """
        soup = self.getSoup(url)
        a = soup.find_all("a")
        return a

    def getClassroom(self):
        """
        获取所有教室信息
        :return: 教室所在校区，name, capacity, type, details
        """
        soup = self.getSoup("http://jiaowu.sicau.edu.cn/web/web/lanmu/jshi.asp")
        r = soup.find_all("td", {"height": "20"})[14:]
        results = []
        urls = a.getUrl("http://jiaowu.sicau.edu.cn/web/web/lanmu/jshi.asp")[7:]
        for i in range(int((len(r) + 1) / 5)):
            results.append({
                "campus": r[5 * i].text.strip(),
                "name": r[5 * i + 1].text.strip(),
                "capacity": r[5 * i + 2].text.strip(),
                "type": r[5 * i + 3].text.strip(),
                "details": "http://jiaowu.sicau.edu.cn/web/web/lanmu/" + urls[2 * i]["href"]
            })
        return results

    def getClassroomDetails(self, url):
        """
        返回教室具体课表
        :param url: 在getClassroom中的details链接
        :return:
        """
        soup = self.getSoup(url)
        r = soup.find_all("td", {"width": "13.5%"})[7:]
        results = []
        for i in range(int((len(r) + 1) / 7)):
            results.append([
                r[7 * i].text.replace(" ", "").replace("\r", "").replace("\n", "").strip(),
                r[7 * i + 1].text.replace(" ", "").replace("\r", "").replace("\n", "").strip(),
                r[7 * i + 2].text.replace(" ", "").replace("\r", "").replace("\n", "").strip(),
                r[7 * i + 3].text.replace(" ", "").replace("\r", "").replace("\n", "").strip(),
                r[7 * i + 4].text.replace(" ", "").replace("\r", "").replace("\n", "").strip(),
                r[7 * i + 5].text.replace(" ", "").replace("\r", "").replace("\n", "").strip(),
                r[7 * i + 6].text.replace(" ", "").replace("\r", "").replace("\n", "").strip()
            ])
        return results

    def getNobodyClassroom(self):
        soup = self.getSoup("http://jiaowu.sicau.edu.cn/web/web/lanmu/kbjshi.asp?bianhao=3350")
        return soup.prettify()

    def getTeachingWeek(self):
        """
        获取当前周数
        :return: 返回周数以list形式
        """
        soup = self.getSoup("http://jiaowu.sicau.edu.cn/web/web/web/index.asp")
        r = re.compile('第(.*)教学周').findall(soup.prettify())
        return r

    def login(self):
        data = {'user': self.studentID, 'pwd': self.password, 'lb': 'S', 'submit': '', 'sign': self.signValue()}
        checkUrl = 'http://jiaowu.sicau.edu.cn/jiaoshi/bangong/check.asp'
        r = self.session.post(checkUrl, data=data, timeout=5, headers=self.headers)
        soup = BeautifulSoup(r.text, features='lxml')
        if soup.find_all("td", {"width": "99"})[0].text == self.studentID:
            return True
        else:
            return False

    def getPersonalInfo(self):
        if self.login() == True:
            url = "http://jiaowu.sicau.edu.cn/xuesheng/dangan/banji/bjiben.asp"
            soup = self.getSoup(url)
            soup_find = soup.find_all("a", {"class": "g_body"})
            results = {
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
            return results

    def getAnnouncement(self):
        """
        获取学校公告
        :return: 公告id, title, area, category, type, date, url
        """
        url = 'http://jiaowu.sicau.edu.cn/web/web/web/gwmore.asp'
        soup = self.getSoup(url)
        titles = []
        urls = []
        fonts = []
        area = []
        category = []
        type = []
        date = re.compile('\((.*)\)').findall(soup.text)[5:]
        results = []
        for i in soup.find_all("a", {"class": "body"}):
            titles.append(i.text)
            urls.append('http://jiaowu.sicau.edu.cn/web/web/web/' + i['href'])
        for font in soup.find_all("font", {"color": "gray"}):
            fonts.append(font.text)
        for i in fonts:
            split = i[1:-1].split("-")
            area.append(split[0])
            category.append(split[1])
            type.append(split[2])
        for i in range(len(titles)):
            results.append({
                "id": str(len(titles) - i),
                "title": titles[i],
                "area": area[i],
                "category": category[i],
                "type": type[i],
                "date": date[i],
                "url": urls[i]
            })
        return results

    def zytongbf(self):
        url = "http://jiaowu.sicau.edu.cn/xuesheng/chengji/chengji/zytongbf.asp"
        soup = self.getSoup(url)
        return soup

if __name__ == '__main__':
    a = Jiaowuchu()
    b = a.zytongbf()
    print(b)
