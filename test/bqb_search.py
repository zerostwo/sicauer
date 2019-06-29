import glob
import itchat
import time
from itchat.content import TEXT, PICTURE
import os

imgs = []
path = os.getcwd()


def searchImage(text):
    print('收到关键词: ', text)
    for name in glob.glob(path + '/bqb/*' + text + '*.*'):
        imgs.append(name)


@itchat.msg_register([PICTURE, TEXT])
def text_reply(msg):
    searchImage(msg.text)
    for img in imgs[:6]:
        # msg.user.send_image(img,'filehelper')
        itchat.send_image(img, toUserName='filehelper')
        # itchat.send_image(img)
        time.sleep(0.3)
        print('开始发送表情：', img)
    imgs.clear()


itchat.auto_login(hotReload=True)
itchat.run()
