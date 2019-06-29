# Date: Fri Jun  7 13:55:18 CST 2019
# Author: duansq
# https://api.sicauer.com/v1/xuegongwang/
# url: http://113.54.11.26/Sys/UserLogin.aspx

import requests
from PIL import Image
import pytesseract
from bs4 import BeautifulSoup
import re

url = "http://113.54.11.26/Sys/UserLogin.aspx"
session = requests.session()

html = session.get('http://113.54.11.26/Sys/default3.aspx')
with open('default3.aspx', 'wb') as file:
    file.write(html.content)

image = Image.open("./picture.png")
image.save("code.png")
image = Image.open("./code.png")
code = pytesseract.image_to_string(image)

r = session.get(url)
soup = BeautifulSoup(r.text, features='lxml')
find_result = soup.find_all("input")
VIEWSTATE = find_result[0]["value"]
EVENTVALIDATION = find_result[1]["value"]
Btn_OK = find_result[-1]["value"]
data = {
    "__VIEWSTATE": "",
    "UserName": "201702420",
    "UserPass": "981211",
    "posx": "1b4cee99ae385c572c44e22ce4a4fddbfaedfc70da128d07444ddc330e2d61e39bc4a33bf48ce2d875f05a75ec97b2c8e2e905c41cad7a387bf63f87b099ae959b1fa08687fa90280c4cbb7c5d33f7eb66e7129a084156fd93a3d399a368d20b4387995f970f5cecf437dc095857996bdae08a324853f238b6664af0a6b6b72e",
    "CheckCode": code,
    "Btn_OK": Btn_OK
}
print(code)
h = re.compile('<input id="posx" name="posx" type="hidden"(.*)>').findall(soup.prettify())
print(h)

RSAKeyPair("010001", "",
           "E0009237BD03B558106299D88B10076B8A7F5228BC93FC27AE36AE4010DADBD1238CA74D5C9757296FA6EF078818E056272117D7C11AE295797E55D029EC6815653291247E4A536C708A672BFDF8AAE0A6D8E4539C9E235BFC6D9CEF0E6EA15A9B7940CB1C272E2A8E62DDF0EB13EB95EE1E50726C0D97954216ABE5D2EC9E45");
encryptedString(key,
    base64encode(strUnicode2Ansi(document.getElementById("UserName").value)) + "\\" +
    base64encode(strUnicode2Ansi(document.getElementById("UserPass").value)));
UserName +"\\"+ UserPass
