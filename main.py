import base64
import json
import os
import random
import time

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def aesDeToken(content, key='Hero590674\0\0\0\0\0\0'):
    key = key[:16].encode('utf-8')
    content = base64.b64decode(content)
    cipher = AES.new(key=key, mode=AES.MODE_ECB)
    res = cipher.decrypt(content)
    res = res[0:-res[-1]]
    return res.decode()


def aesEnToken(content, key='Hero590674\0\0\0\0\0\0'):
    key = key[:16].encode('utf-8')
    cipher = AES.new(key=key, mode=AES.MODE_ECB)
    content = pad(content.encode(), 16)
    res = cipher.encrypt(content)
    return base64.b64encode(res).decode('utf-8')


# 随机数组件
def generate_random_str(randomlength=16):
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str

def getFileContent(path):
    if os.path.exists(path) and os.path.isfile(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    else:
        raise Exception(f'无法找到文件：{path}')

def initGameConfig():
    url = 'https://comm.ams.game.qq.com/ide/page/90_Vbx2Yd'
    head = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': ck
    }
    res = requests.get(url=url, headers=head).text
    js = json.loads(res)
    print(res)
    flows = js['flows']
    for key in flows.keys():
        item = flows[key]
        sIdeToken = item['sIdeToken']
        sName = item['sName']
        if sName == '[h5]游戏开始':
            startGameConfig['iChartId'] = key
            startGameConfig['iSubChartId'] = key
            startGameConfig['sIdeToken'] = sIdeToken
        elif sName == '[h5]游戏结算':
            sumbitGameScore['iChartId'] = key
            sumbitGameScore['iSubChartId'] = key
            sumbitGameScore['sIdeToken'] = sIdeToken
        elif sName == '[H5]初始化':
            initConfig['iChartId'] = key
            initConfig['iSubChartId'] = key
            initConfig['sIdeToken'] = sIdeToken

def init():
    url = 'https://comm.ams.game.qq.com/ide/'
    head = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': ck
    }
    data = {
        'iChartId': initConfig['iChartId'],
        'iSubChartId': initConfig['iSubChartId'],
        'sIdeToken': initConfig['sIdeToken'],
        'sArea': sArea,
        'sPlatId': sPlatId,
        'acctype': acctype,
        'e_code': '0',
        'g_code': '0',
        'eas_url': 'http%3A%2F%2Fgn.qq.com%2Fact%2Fa20231103through2%2F',
        'eas_refer': 'http%3A%2F%2Fgn.qq.com%2Fact%2Fa20231103through2%2F%3Freqid%3Ded30a95a-0fe0-4ceb-8c7b-81980a724bc2%26version%3D27'
    }
    res = requests.post(url=url, headers=head, data=data).text
    js = json.loads(res)
    print(res)

def startGame():
    url = 'https://comm.ams.game.qq.com/ide/'
    head = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': ck
    }
    data = {
        'iChartId': startGameConfig['iChartId'],
        'iSubChartId': startGameConfig['iSubChartId'],
        'sIdeToken': startGameConfig['sIdeToken'],
        'sArea': sArea,
        'sPlatId': sPlatId,
        'acctype': acctype,
        'e_code': '0',
        'g_code': '0',
        'eas_url': 'http%3A%2F%2Fgn.qq.com%2Fact%2Fa20231103through2%2F',
        'eas_refer': 'http%3A%2F%2Fgn.qq.com%2Fact%2Fa20231103through2%2F%3Freqid%3D1428e2f2-604b-4d06-84c9-ac926f652d40%26version%3D27'
    }
    res = requests.post(url=url, headers=head, data=data).text
    js = json.loads(res)
    print(res)
    return js['jData']['nonce']

def postScore(score=400):
    noce = aesEnToken(startGame())
    print("玩游戏20秒，请耐心等待...")
    time.sleep(20)
    url = 'https://comm.ams.game.qq.com/ide/'
    head = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': ck
    }
    data = {
        'iChartId': sumbitGameScore['iChartId'],
        'iSubChartId': sumbitGameScore['iSubChartId'],
        'sIdeToken': sumbitGameScore['sIdeToken'],
        'sArea': sArea,
        'sPlatId': sPlatId,
        'acctype': acctype,
        'score': score,
        'nonce': noce,
        'e_code': '0',
        'g_code': '0',
        'eas_url': 'http%3A%2F%2Fgn.qq.com%2Fact%2Fa20231103through2%2F',
        'eas_refer': 'http%3A%2F%2Fgn.qq.com%2Fact%2Fa20231103through2%2F%3Freqid%3Da31baabc-8d98-48d0-8cad-070dd06fc4c1%26version%3D27'
    }
    res = requests.post(url=url, headers=head, data=data).text
    print(res)

if __name__ == '__main__':
    ck = getFileContent('./gnck.txt')
    startGameConfig = {
        'iChartId': '',
        'iSubChartId': '',
        'sIdeToken': '',
    }
    sumbitGameScore = {
        'iChartId': '',
        'iSubChartId': '',
        'sIdeToken': '',
    }
    initConfig = {
        'iChartId': '',
        'iSubChartId': '',
        'sIdeToken': '',
    }
    '''
    平台 0=ios 1=安卓
    '''
    sPlatId = '1'
    '''
    分区 wx qq
    '''
    acctype = 'qq'
    '''
    分区 2=qq 1=微信
    '''
    sArea = '2'
    '''
    提交的分数
    '''
    sumbitScore = 400
    initGameConfig()
    init()
    postScore(sumbitScore)
