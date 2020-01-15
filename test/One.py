import requests
from bs4 import BeautifulSoup
import os


def one(num):
    url = "http://wufazhuce.com/one/{num}".format(num=num)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    oneCitaSoup = soup.find_all("div", {"class": "one-cita"})
    daySoup = soup.find_all("p", {"class": "dom"})
    yearMonth = soup.find_all("p", {"class": "may"})
    monthConver = {
        "Jan": "1",
        "Feb": "2",
        "Mar": "3",
        "Apr": "4",
        "May": "5",
        "Jun": "6",
        "Jul": "7",
        "Aug": "8",
        "Sep": "9",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12"
    }
    day = daySoup[0].text
    month = monthConver[yearMonth[0].text.split()[0]]
    year = yearMonth[0].text.split()[1]
    oneCita = oneCitaSoup[0].text.strip()
    oneImage = soup.find_all("div", {"class": "one-imagen"})
    date = year + "-" + month + "-" + day
    path = os.getcwd()
    src = oneImage[0].img.get('src')
    img = requests.get(src)
    with open(path + "/oneImage/" + oneCita + ".jpg", 'wb') as f:
        f.write(img.content)
    return date + "|" + oneCita

if __name__ == '__main__':
    for i in range(14, 100):
        try:
            fp = open("./one.txt", 'a')
            print(one(i), file=fp)
            fp.flush()
            fp.close()
            print(one(i))
        except:
            pass