import requests


class Isicau:
    loginName = "201702420"
    password = "1314159@Dd"
    headers1 = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'jk.sicau.edu.cn',
        'pu-version': '1.1.1',
        'User-Agent': 'PocketUniversity/1.1.1 (iPad; iOS 12.2; Scale/2.00)',
    }

    def isicau(self):
        data = {
            "loginName": self.loginName,
            "password": self.password,
            "sid": "f1c97a0e81c24e98adb1ebdadca0699b"
        }
        session = requests.session()
        r = session.post('https://jk.sicau.edu.cn/user/login/v1.0.0/snoLogin', data=data, headers=self.headers1)
        schoolActListUrl = "https://jk.sicau.edu.cn/act/actInfo/v1.0.0/getUserSchoolActList"
        headers2 = {
            'Content-Type': 'multipart/form-data; boundary=Boundary+7A02C92264A7392E',
            'Host': 'jk.sicau.edu.cn',
            'User-Agent': 'PocketUniversity/1.1.1 (iPad; iOS 12.2; Scale/2.00)',
            'pu-version': '1.1.1',
            'x-access-token': r.json()['content']['token'],
        }
        getUserSchoolActList = session.post(schoolActListUrl, headers=headers2)
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
            })
        return actives


if __name__ == '__main__':
    inquire = Isicau()
    print(inquire.isicau())
