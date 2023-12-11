import base64
import datetime
import json
import os
import random
import sys
import time

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from urllib.parse import quote, unquote

def printf(text, userId=''):
    ti = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    print(f'[{ti}][{userId}]: {text}')
    sys.stdout.flush()
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
    printf(res)
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
        elif sName == '[h5]分享':
            shareConfig['iChartId'] = key
            shareConfig['iSubChartId'] = key
            shareConfig['sIdeToken'] = sIdeToken
        elif sName == '[H5]任务领奖':
            taskConfig['iChartId'] = key
            taskConfig['iSubChartId'] = key
            taskConfig['sIdeToken'] = sIdeToken

def shareDay():
    url = 'https://comm.ams.game.qq.com/ide/'
    head = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': ck
    }
    data = {
        'iChartId': shareConfig['iChartId'],
        'iSubChartId': shareConfig['iSubChartId'],
        'sIdeToken': shareConfig['sIdeToken'],
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
    printf(res)

def taskRecive(taskId):
    url = 'https://comm.ams.game.qq.com/ide/'
    head = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': ck
    }
    data = {
        'iChartId': taskConfig['iChartId'],
        'iSubChartId': taskConfig['iSubChartId'],
        'sIdeToken': taskConfig['sIdeToken'],
        'iTaskId': taskId,
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
    printf(res)
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
    if js['ret'] == 101:
        printf(js['sMsg'])
        exit()
    if js['ret'] == 1:
        printf(js['sMsg'] + '查询游戏角色为空，未注册游戏或平台选错，请手动修改main.py最下面的代码选择安卓 ios端及wx或qq区')
        exit()
    return js

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
    printf(res)
    try:
        return js['jData']['nonce']
    except Exception:
        printf('开始游戏失败，未注册游戏或平台选错，请手动修改main.py最下面的代码选择安卓 ios端及wx或qq区')

def postScore(score=400):
    noce = aesEnToken(startGame())
    printf("玩游戏5秒，请耐心等待...")
    time.sleep(5)
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
    js = json.loads(res)
    if js['ret'] == 0 and js['sMsg'] == 'succ':
        printf(f'分数提交成功：{js["jData"]["score"]}分 可用总分：{js["jData"]["teamScore"]}分')
    printf(res)

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
    shareConfig = {
        'iChartId': '',
        'iSubChartId': '',
        'sIdeToken': '',
    }
    taskConfig = {
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
    res = init()
    if res['ret'] == 0 and res['sMsg'] == 'succ':
        jData = res['jData']
        arrTask = jData['arrTask']
        nickName = jData['nickName']
        printf(f'欢迎英雄使用[{unquote(nickName)}]')
        printf(f'开始做每天分享任务')
        shareDay()
        for it in arrTask:
            name = it['name']
            reddotTaskId = it['reddotTaskId']
            printf(f'开始领取任务奖励 [{name}]')
            taskRecive(reddotTaskId)
        res = init()
        ticket = res['jData']['ticket']
        printf(f'任务完成 可突围次数：{ticket} 开始玩游戏提交成绩')
        for i in range(1, int(ticket)+1):
            postScore(sumbitScore)
            printf(f'第{i}次提交成绩完成')
        res = init()
        teamScore = res['jData']['teamScore']
        printf(f'执行完毕 可用总积分：{teamScore}')
