import requests
import json


class GetStart:
    loginName = "201702420"
    password = "1314159@Dd"
    session = requests.session()
    getTokenHeaders = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'jk.sicau.edu.cn',
        'pu-version': '1.1.1',
        'User-Agent': 'PocketUniversity/1.1.1 (iPad; iOS 12.2; Scale/2.00)',
    }

    def headers(self):
        data = {
            "loginName": self.loginName,
            "password": self.password,
            "sid": "f1c97a0e81c24e98adb1ebdadca0699b"  # 川农的sid编号
        }
        r = self.session.post('https://jk.sicau.edu.cn/user/login/v1.0.0/snoLogin', data=data,
                              headers=self.getTokenHeaders)
        headers = {
            # 'Content-Type': 'multipart/form-data; boundary=Boundary+7A02C92264A7392E',
            'Host': 'jk.sicau.edu.cn',
            'User-Agent': 'PocketUniversity/1.1.1 (iPad; iOS 12.2; Scale/2.00)',
            'pu-version': '1.1.1',
            'x-access-token': r.json()['content']['token'],
        }
        return headers

    def crack(self):
        data = {
            "loginName": self.loginName,
            "password": self.password,
            "sid": "f1c97a0e81c24e98adb1ebdadca0699b"  # 川农的sid编号
        }
        r = self.session.post('https://jk.sicau.edu.cn/user/login/v1.0.0/snoLogin', data=data,
                              headers=self.getTokenHeaders, timeout=5)
        return r.json()['content']['name']


class Isicau(GetStart):
    def getUserSchoolActList(self):
        url = "https://jk.sicau.edu.cn/act/actInfo/v1.0.0/getUserSchoolActList"
        data = {
            "page": 2
        }
        getUserSchoolActList = self.session.post(url, data=data, headers=self.headers())
        content = getUserSchoolActList.json()['content']
        actives = []
        for i in range(len(content)):
            active = content[i]
            actives.append({
                "title": active["title"],
                "typeName": active["typeName"],
                'addr': active['addr'],
                'canJoin': active['canJoin'],
                "startTime": active['startTime'],
                # "startUser": active['startUser'],
                # "startUserName": active["startUserName"],
                # "status": active['status'],
                "statusName": active['statusName'],
                "id": active['id']
            })
        return actives

    def actDetail(self, actId):
        url = 'https://jk.sicau.edu.cn/act/actInfo/v1.0.0/getActDetail'
        data = {
            "actId": actId
        }
        getActDetail = self.session.post(url=url, data=data, headers=self.headers())
        return getActDetail.json()["content"]

    def getHomePageApps(self):
        """
        获取主页功能信息。包括：封面人物、互动交流、全校活动、申请学分、本校部落和后勤报修。
        {
            'code': '0',
            'message': '成功',
            'content': {
            'Four': [
                {
                    'id': 'b0a9be8286694ba9a09de92e494caf02',
                    'appName': '封面人物',
                    'logo': 'https://file.sicau.edu.cn/userfiles/home/app/953bbfce2df24a65ae5f577ebbaa3dad.png',
                    'description': '',
                    'appIndex': 1,
                    'linkType': '0',
                    'originalLinkAddress': 'coverPeople',
                    'originalLinkParam': '', 'hurl': ''
                },
            ]
        }
        :return:
        """
        url = 'https://jk.sicau.edu.cn/user/homePage/v1.0.0/getHomePageApps'
        data = {
            "clientType": "1",
            "version": "V1.1.1"
        }
        getHomePageApps = self.session.post(url, data=data, headers=self.headers())
        return getHomePageApps.json()

    def getFloorsInfo(self):
        """
        获取推荐活动和校园资讯。
        :return:
        """
        url = 'https://jk.sicau.edu.cn/user/homePage/v1.0.0/getFloorsInfo'
        data = {
            "clientType": "1",
            "version": "V1.1.2"
        }
        getFloorsInfo = self.session.post(url, data=data, headers=self.headers())
        return getFloorsInfo.json()

    def getSchoolBroadCast(self):
        """
        获取学校广播信息。
        {
            'code': '0',
            'message': '',
            'content': {
                'PU': {
                    'id': '1032',
                    'noticeTitle': '关于i川农升级至1.1.2版本的通知',
                    'noticeContent': None,
                    'noticeType': '1',
                    'publishDate': '2019年02月27日',
                    'publishBy': None,
                    'readFlag': None,
                    'skipType': '1',
                    'skipAddress': 'https://h5.sicau.edu.cn/imgText/index.html',
                    'skipParam': '',
                    'hurl': 'https://h5.sicau.edu.cn/imgText/index.html?uid=20046122&snId=8GVKMzr14Dw='
                },
            'SN': {
                'id': '782',
                'noticeTitle': '关于准时参加二课活动的通知',
                'noticeContent': None,
                'noticeType': '1',
                'publishDate': '2018年12月19日',
                'publishBy': None,
                'readFlag': None,
                'skipType': '1',
                'skipAddress': 'https://h5.sicau.edu.cn/imgText/index.html',
                'skipParam': '',
                'hurl': 'https://h5.sicau.edu.cn/imgText/index.html?uid=20046122&snId=b+nLl/GeahY='
                }
            }
        }
        :return:
        """
        url = 'https://jk.sicau.edu.cn/msg/MessageFrontPageController/v1.0.0/getSchoolBroadCast'
        data = {
            "clientType": "1",
        }
        getSchoolBroadCast = self.session.post(url, data=data, headers=self.headers())
        return getSchoolBroadCast.json()

    def getNewVersion(self):
        """
        获取新版本。
        :return:
        """
        url = "https://jk.sicau.edu.cn/user/setting/v1.0.0/getNewVersion"
        data = {
            "clientType": "1",
            "versionCode": "V1.1.2"
        }
        getNewVersion = self.session.post(url, data=data, headers=self.headers())
        return getNewVersion.json()

    def getUnreadCount(self):
        """
        获取未读消息数量。
        {
            'code': '0',
            'message': '成功',
            'content': {
                'systemCount': 0,
                'schInfoCount': 0,
                'schoolCount': 0,
                'puCount': 0}
        }
        :return:
        """
        url = "https://jk.sicau.edu.cn/msg/MessageFrontPageController/v1.0.0/getUnreadCount"
        data = {
            "clientType": "1",
        }
        getUnreadCount = self.session.post(url, data=data, headers=self.headers())
        return getUnreadCount.json()

    def getUserInfo(self):
        """
        获取用户信息。
        :return:
        """
        url = "https://jk.sicau.edu.cn/user/frontPage/v1.0.0/getUserInfo"
        getUserInfo = self.session.post(url, headers=self.headers())
        return getUserInfo.json()

    def getMeFollowList(self):
        """
        获取关注自己的用户列表。
        :return:
        """
        url = "https://jk.sicau.edu.cn/user/follow/v1.0.0/getMeFollowList"
        # data = {
        #     "count": "20",
        #     "startCount": "0"
        # }
        getMeFollowList = self.session.post(url, headers=self.headers())
        return getMeFollowList.json()

    def getQRCode(self):
        """
        获取二维码。
        :return:
        """
        url = "https://jk.sicau.edu.cn/user/frontPage/v1.0.0/getQRCode"
        getQRCode = self.session.post(url, headers=self.headers())
        return getQRCode.json()

    def getVisitorList(self):
        """
        获取访客列表。
        :return:
        """
        url = "https://jk.sicau.edu.cn/user/visit/v1.0.0/getVisitorList"
        data = {
            "count": "20",
            "startCount": "0"
        }
        getVisitorList = self.session.post(url, data=data, headers=self.headers())
        return getVisitorList.json()


if __name__ == '__main__':
    a = Isicau()
    b = a.getUserSchoolActList()
    print(b)
