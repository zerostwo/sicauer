import os

import requests
from bs4 import BeautifulSoup

url = 'https://fabiaoqing.com/biaoqing/lists/page/{page}.html'
urls = [url.format(page=page) for page in range(1, 200 + 1)]
for i in urls:
    r = requests.get(i)
    soup = BeautifulSoup(r.content, 'lxml')
    img_list = soup.find_all('img', class_='ui image lazy')
    path = os.getcwd()
    for img in img_list:
        image = img.get('data-original')
        title = img.get('title')
        # print(image)
        try:
            with open(path + "/bqb/" + title + os.path.splitext(image)[-1], 'wb') as f:
                img = requests.get(image).content
                f.write(img)
        except:
            print(image)
