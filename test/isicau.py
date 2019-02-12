import requests


def isicau():
    headers1 = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'jk.sicau.edu.cn',
        'pu-version': '1.1.1',
        'User-Agent': 'PocketUniversity/1.1.1 (iPad; iOS 12.2; Scale/2.00)',
    }
    data = {
        "loginName": "201702420",
        "password": "1314159@Dd",
        "sid": "f1c97a0e81c24e98adb1ebdadca0699b"
    }
    session = requests.session()
    r = session.post('https://jk.sicau.edu.cn/user/login/v1.0.0/snoLogin', data=data, headers=headers1)
    getVisitorList_url = 'https://jk.sicau.edu.cn/user/visit/v1.0.0/getVisitorList'
    getUserSchoolActList_url = "https://jk.sicau.edu.cn/act/actInfo/v1.0.0/getUserSchoolActList"
    headers2 = {
        'Content-Type': 'multipart/form-data; boundary=Boundary+7A02C92264A7392E',
        'Host': 'jk.sicau.edu.cn',
        'User-Agent': 'PocketUniversity/1.1.1 (iPad; iOS 12.2; Scale/2.00)',
        'pu-version': '1.1.1',
        'x-access-token': r.json()['content']['token'],
    }
    getVisitorList = session.post(getVisitorList_url, headers=headers2)
    getUserSchoolActList = session.post(getUserSchoolActList_url, headers=headers2)
    # return getVisitorList.json()
    return getUserSchoolActList.json()


if __name__ == '__main__':
    print(isicau())
