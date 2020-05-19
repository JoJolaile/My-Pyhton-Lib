import requests
import bs4
import urllib.request
import urllib.parse
import json
import random
import os
import you_get
import time

# 登陆congnitiveclass.ai课程主界面
classurl = 'https://courses.cognitiveclass.ai/courses/course-v1:CognitiveClass+ML0101ENv3+2018/courseware/bd64ccdf56ad4ea1afe870e26d583038/eb6af21484a94f07a500271fa4c82ea4/'

path = '/Users/zhaomiao/Desktop/Machine Learning by  Python'

USER_AGENTS = [
    "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1"
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 "
    "Safari/534.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 "
    "Safari/535.11",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR "
    "3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 "
    "TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 "
    "LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR "
    "3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; "
    "360SE)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X "
    "MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 5.0; Windows NT)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12 "]

def run():

    #获得cookie，以便之后登陆用
    Cookies = getCookie()

    #访问网站
    result = getwebinfo(classurl,Cookies)

    # 找出包含视频课程的网页链接，
    classlist = result.find_all('div', class_="menu-item")
    list = []
    classmenu = []
    for each in classlist:
        if '(' in each.p.text:
            list.append(each.a.attrs['href'])
            classmenu.append(each.p.text)
    print('下载文件总数： ' + str(len(list)))
    print(classmenu)
    file = open(path +'/classmenu.txt', 'w')
    file.writelines(classmenu)
    file.close

    for subclass in list:
        #访问每个课程网站的网页
        subclassurl = 'https://courses.cognitiveclass.ai' + subclass
        soup = getwebinfo(subclassurl,Cookies)
        #获得视频链接
        url = soup.find_all('div', class_="seq_contents tex2jax_ignore asciimath2jax_ignore")
        videourl = \
        url[0].text.replace('\n', ' ').split('">Download video')[0].split('download-button">             <a href="')[1]
        srt = \
        url[0].text.replace('\n', ' ').split('video-tracks video-download-button">             <a href="')[1].split('">Download transcript')[0]

        srturl = 'https://courses.cognitiveclass.ai' + srt

        # 获取视频列表并编辑list为以下格式 http://videos.bigdatauniversity.com/ML0101ENv3/videos/Intro%20to%20Regression.mp4

        print(videourl)
        cmd = 'you-get ' + '-o "' + path + '" "' + videourl.replace(' ', '%20') + '"'
        print(cmd)
        os.system(cmd)

        # you-get获得字幕不成功，需要打开字幕网页的方式
        headers = {}
        headers['User-Agent'] = random.choice(USER_AGENTS)
        headers['Cookie'] = Cookies
        subs = requests.get(srturl, headers=headers)
        subcontent = bs4.BeautifulSoup(subs.text, 'html.parser')
        subfile = open(path + '/' + videourl.split('videos/')[1].split('.mp4')[0].replace('%20',' ') +'.txt', 'w')

        # 写出到文件
        subfile.write(subcontent.text)
        subfile.flush();
        subfile.close

        # 睡眠一下
        time.sleep(5)


def getwebinfo(classurl,cookies):
    # 反反爬虫，增加header模拟浏览器访问
    headers = {}
    headers['User-Agent'] = random.choice(USER_AGENTS)
    #使用cookie登陆，
    #headers['Cookie'] = 'sessionid=bd6xkdh18cudctytye3t6wbf4lizlxh3;csrftoken=7yfhiWkWQdTBLRCzvhXZ5YK7px1FSaUh'
    headers['Cookie'] = cookies
    res = requests.get(classurl, headers=headers)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    return soup


def getCookie():

    url = 'https://courses.cognitiveclass.ai/user_api/v1/account/login_session/'

    headers = {}
    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    headers['Pragma'] = 'no-cache'
    headers['Accept'] = '*/*'
    headers['Accept-Encoding'] = 'br, gzip, deflate'
    headers['Host'] = 'courses.cognitiveclass.ai'
    headers['Accept-Language'] = 'zh-cn'
    headers['Cache-Control'] = 'no-cache'
    headers['Origin'] = 'https://courses.cognitiveclass.ai'
    headers['User-Agent'] = random.choice(USER_AGENTS)
    headers['Content-Length'] = '55'
    headers['Referer'] = 'https://courses.cognitiveclass.ai/login'
    headers['Connection'] = 'keep-alive'
    headers['Cookie'] = '_gat=1; ajs_anonymous_id=%22d86e2f2c-ff78-44b1-a1fc-e65aab625cda%22; uvts=5e1f016d-cf16-44f0-4867-855f9f68a7cd; notice_behavior=implied|eu; ajs_group_id=null; ajs_user_id=%22IBMid-270004F249%22; optimizelyEndUserId=oeu1584073020581r0.41181253485689073; _ga=GA1.2.1783215637.1584072866; _gid=GA1.2.1548702394.1584072866; csrftoken=cUwMODU3kgDQbuzn7tJFm59OafylQJDn; _vwo_uuid_v2=D7171352D199829AB7F2A555A8E6E7B1D|e738d5114ec2fcb0be46d2ccd71aba4d; uvts=225652b5-6914-4a0d-4451-15bd71443d74; sessionid=h66hlgpok9f11wmvpbo21r6e5ehoi64h'
    headers['X-Requested-With'] = 'XMLHttpRequest'
    headers['X-CSRFToken'] = 'cUwMODU3kgDQbuzn7tJFm59OafylQJDn'

    data = {}
    data['MIME 类型'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    data['email'] = 'zhmiao@cn.ibm.com'
    data['password'] = 'Miaowen17'
    data['remember'] = 'false'

    req = requests.post(url=url, data=data, headers=headers)
    ck = '; '.join(['='.join(item) for item in req.cookies.items()])
    return ck



#迅雷下载过于复杂，弃用，使用python直接下载
# def CrXunlei(videourl,filenm):
#     print('xunlei')
#
#     url = 'http://homecloud.remote.xiazaibao.xunlei.com/createBtTask?pid=001CC227DE9B775X0001&v=2&ct=0&callback=window.parent._POST_CALLBACK_4_'
#
#     headers = {}
#
#     headers['User-Agent'] = random.choice(USER_AGENTS)
#     headers['Referer'] = 'http://yc.xzb.xunlei.com/'
#     headers['Origin'] = 'http://yc.xzb.xunlei.com'
#     headers['Content-Type'] = 'application/x-www-form-urlencoded'
#     headers['Cache-Control'] = 'no-cache'
#     headers['Pragma'] = 'no-cache'
#     headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
#     headers['Upgrade-Insecure-Requests'] = '1'
#
#     headers['Cookie'] = 'sessionid=ws001.15A25AB0D1940D53E014B25F3BBA30C8;userid=335844876'
#
#     rawdata = '{"path":"C:/TDDOWNLOAD/","infohash":"' + videourl + '","name":"' + filenm + '","btSub":[0,1,2,3],"loalfile":""}'
#
#     data = "json=" + urllib.parse.quote(rawdata)
#
#     req = requests.post(url=url, data=data, headers=headers)

if __name__ == "__main__":
    run()