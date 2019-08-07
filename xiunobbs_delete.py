import requests
from lxml import html
import re

#=======================================================================================================================
# config
#=======================================================================================================================
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    }
data = {
    'mobile':'your username',   
    'password':'your password', # md5 过以后的值
}
loginUrl ='https://www.scboy.com/?user-login.htm'

# 略过的回帖 ID
postFilter = []
# 略过的主题 ID
threadFilter = []

# 回帖页数
postNum = 0
# 主题页数
threadNum = 0
#=======================================================================================================================

def deletePost(session, id):
    if (postFilter.count(id) != 0):
        return
    session.post('https://www.scboy.com/?post-update-'+ str(id) +'.htm', headers = headers, data={
        'quotepid': id,
        'message': '\u200b',
        'doctype': '0',
    }, verify=False)


def deleteThread(session, id):
    if (threadFilter.count(id) != 0):
        return
    session.post('https://www.scboy.com/?post-update-'+ id +'.htm', headers = headers, data={
        'update_reason': '',
        'tagid[]': '1',
        'tagid[]': '1',
        'tagid[]': '1',
        'tagid[]': '1',
        'tagid[]': '1',
        'tagid[]': '1',
        'tagid[]': '1',
        'tagid[]': '1',
        'tagid[]': '1',
        'tagid[]': '1',
        'tagid[]': '1',
        'subject': '\u200b',
        'quotepid': '0',
        'message': '\u200b',
        'haya_poll_type': '0',
        'haya_poll_max_num': '1',
        'fid': '1',
        'doctype': '0',
    }, verify=False)


def deleteAllPost(session, num):
    for num in range(1, num + 1):
        url = 'https://www.scboy.com/?my-post-'+ str(num) +'.htm'
        response = session.get(url, headers = headers, verify=False)
        tree = html.fromstring(response.text) 
        paths = tree.xpath('//div[@class="d-flex justify-content-between small text-muted"]/div[@class="text-right text-grey"]/a[@class="text-grey post_update mr-2"]/@href')
        paths = list(map(lambda x: "https://www.scboy.com/" + x, paths))
        for path in paths:
            matchObj = re.match(r'\?post-update-([0-9]*)', path)
            if(matchObj):
                deletePost(session, matchObj.group(1))


def deleteAllThread(session, num):
    for num in range(1, num + 1):
        url = 'https://www.scboy.com/?my-thread-'+ str(num) +'.htm'
        response = session.get(url, headers = headers, verify=False)
        tree = html.fromstring(response.text) 
        paths = tree.xpath('//li[@class="media thread tap  "]/div[@class="media-body"]/div[@class="subject break-all"]/a/@href')
        paths = list(map(lambda x: "https://www.scboy.com/" + x, paths))
        for path in paths:
            matchObj = re.match(r'https://www.scboy.com/\?thread-([0-9]*)', path)
            if(matchObj):
                response = session.get(path, headers = headers, verify=False)
                tree = html.fromstring(response.text) 
                threadPath = tree.xpath('//div[@class="card card-thread"]//div[@class="media-body"]//a[@class="text-grey mr-2 post_update"]/@href')
                deleteThread(session, re.match(r'\?post-update-([0-9]*)', threadPath[0]).group(1))


def main():
    session = requests.Session()
    session.post(loginUrl,headers = headers,data = data, verify=False)
    deleteAllThread(session, threadNum)
    deletePost(session, postNum)

main()
