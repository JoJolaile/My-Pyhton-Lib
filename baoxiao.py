

'''
公司网站登陆后的cookie在报销时使用不成功，跳转过多，放弃自动获得，采用以下方法
1 登陆报销网站，上传一张图票，使用检查元素，找到上传图片的url和cookie
2 使用url获得empkey，更新createreport的data部分的值
3 图片上传到服务器后，为避免重复识别浪费次数，将图片信息写到了文本，可通过读取文本继续执行
注意每次upload的url会变，crereport和creitem的不会
注意有时附加税扫不出来，结果还是要确认
照相时，必须使用qq程序内部拍照，苹果系统自带相机照片不识别
'''

from aip import AipOcr
import time
import os
import requests
import time
import random
from requests_toolbelt.multipart.encoder import MultipartEncoder
import re
import base64
#import ssl
import json
import urllib

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

# 每次需要修改
uploadurl = 'https://www.concursolutions.com/expense/ExpenseDotNet/Receipts/UploadLineItemImage.ashx?ickey=2&EmpKey=gWtfLpFQ8gYT8XlN4olC9ZIc0vBKl5uI'
# 不需要修改，
creReporturl = 'https://www.concursolutions.com/expense/expenseDotNet/Proxy/expenseRouter.ashx?requests=ExpenseReport%3ASaveReport&entityId=gWqZH%24pXAEGREJokKQKMbrfRcPKgZo6iUgNxJ7lL0&cuuid=gWkF7%24sAtjcNicDWEVXQMWl%24piIElFVWPs3REB2bIQP9p4GW9tg'
creItemrul  = 'https://www.concursolutions.com/expense/expenseDotNet/Proxy/expenseRouter.ashx?requests=ExpenseReport%3ASaveExpense&entityId=gWqZH%24pXAEGREJokKQKMbrfRcPKgZo6iUgNxJ7lL0&cuuid=gWkF7%24sAtjcNicDWEVXQMWl%24piIElFVWPs3REB2bIQP9p4GW9tg'

EmpKey = uploadurl.split('EmpKey=')[1]

headers = {}

headers['Pragma'] = 'no-cache'
headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
headers['Host'] = 'www.concursolutions.com'
headers['Accept-Language'] = 'zh-cn'
headers['Cache-Control'] = 'no-cache'
headers['Accept-Encoding'] = 'br, gzip, deflate'
headers['Origin'] = 'https://www.concursolutions.com'
headers['Referer'] = 'https://www.concursolutions.com/expense/client/default.asp'
headers['User-Agent'] = random.choice(USER_AGENTS)
headers['Connection'] = 'keep-alive'
headers['Cookie'] = 'bm_sv=C9EC63F7AFC23C2D4155A149EB17E968~HJ12ny0aD2BirwSkTjkd3wJthEv8PmeonJsvPg2K5Xs9FerjOMP3hOq2Rlu3kuKYxjVX0udcEhc1uTQQuaoWafK/FpE1gcPXIbCBLfYFh4eNZLKkSlxTJBMIEI62uIjcVRYnKkgYMUvdb0gqoAm3EJaGq4dB3d91Ui0zjtxMgmI=; _ga=GA1.2.1604543426.1584673223; _gid=GA1.2.1065059991.1584673223; CteMtRequestId=3%2F19%2F2020%2D82829%2E14; _gat=1; JWT=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjE0NTU2MTQwMjIifQ.eyJjb25jdXIuc2NvcGVzIjpbIioiXSwiYXVkIjoiKiIsImNvbmN1ci5wcm9maWxlIjoiaHR0cHM6Ly91cy5hcGkuY29uY3Vyc29sdXRpb25zLmNvbS9wcm9maWxlL3YxL3ByaW5jaXBhbHMvMDhlYzUwNjAtNGFlOS00MjY0LTk1YzAtZTRkYzdmM2MzZDY1IiwiY29uY3VyLnZlcnNpb24iOjMsImNvbmN1ci50eXBlIjoidXNlciIsImNvbmN1ci5hcHAiOiJodHRwczovL3VzLmFwaS5jb25jdXJzb2x1dGlvbnMuY29tL3Byb2ZpbGUvdjEvYXBwcy80Y2I4Y2M2Mi1hNzEzLTRhMjgtOGNlMC00ZDk2Zjc4Yzk4MDMiLCJzdWIiOiIwOGVjNTA2MC00YWU5LTQyNjQtOTVjMC1lNGRjN2YzYzNkNjUiLCJpc3MiOiJodHRwczovL3VzLmFwaS5jb25jdXJzb2x1dGlvbnMuY29tIiwiZXhwIjoxNTg0Njc2ODEzLCJjb25jdXIuYXBwSWQiOiI0Y2I4Y2M2Mi1hNzEzLTRhMjgtOGNlMC00ZDk2Zjc4Yzk4MDMiLCJuYmYiOjE1ODQ2NzMyMTMsImlhdCI6MTU4NDY3MzIxMywiY29uY3VyLmNvbXBhbnkiOiIwMWM0Yzc4Ny01MzVmLTQ3MzYtYWQ2Zi1lYzJjOTAxZmVhY2UifQ.cw7044g4zVKyoTlJBSgZ4rLQgI6DHSBU0G9JyA8iP1bmiY6oxobILN-vDr5HV-D7zgAZ9uey4xBBtJ3TEaYvAgCM7F3m8VbraFwqSi37s5QnHPLTjRmXfxfemPn5frnLnAe335q_dL3J4Ko3qlBgDWFBDpwg5wbL0TvLbAz3TkSo2EfmQe6OjIaDluhyOi2E4-t7s-rXX6uBiyFMLboZrT36ccwq2dzVCGbxrYMPMWrDw0pA6kqccHYYPpS-YT--RuTJ7UysxUXgF3iWHUe0IAoyrxap4f44Rg7bl-viJL4xsaHjqyEdYqhOr_fNEz48K47d1UtHtj9es3d3XzwGJA; OTSESSIONAABQRD=78D07A21G5D44G45D4GBFE7GA06740969320; Login=LoginURL=https%3A%2F%2Fw3id.sso.ibm.com%2Fauth%2Fsps%2Fsamlidp%2Fsaml20%2Fsloinitial&LastLoginName=; OTDefaultLang=zh-cn; OTLang=zh-cn; OTSESSIONAABQRN=78D07A21G5D44G45D4GBFE7GA06740969320; brandingid=12; _abck=F99ACC146EC12EA551336833FC3C7EA6~0~YAAQ9NfSFwwrOp5wAQAAW1Pi9QPFFmpW6wAXdLuKVa6uEgbTqKYNxKbRnbB3ghP2DvSSN5kCy+9ZuFg39pL7KW1fqCGhD39RvEj4Jx9WtasFAarExWFNJREepDOCgkZL4AI001h7sKy7zQDZTy9ecnLI+bsNLsJhgZoq30WIidYH75Z384A4gORgWI9JxdPEuzhvkBzOE8Xf34mP/tXBvdjqvhDHE+XmhWH3ssx2rrbjkRm12PSui8RYc92Vg5cLZlbnNeMiRLMgxOq8ZQ21u48/8Nx+QX8rZ/MqlQ8JFiZ+HZC/bL6lKTrBdyLyOEH2tbLGv1YSjBAQN7PtCvGSEw==~-1~-1~-1; ak_bmsc=9B94A236C3A5A99783D993E273FFB13417D2D7F495530000BD31745EFD434C21~plpHS+mKPjIl67UXRObMc/mKMrtmdSliHXv1W4mls8QfikNCMUf6OUKCQioVViqz/crjycAYLAwPyzkH/zwXqXCgmSMfKuEJvD8GFvKVmavWYzeqZUPjMhWWalJNHFLVhB2bEgeHnCUF+ennCHW7et6mWs59lAe7Hl7JbI+CssaVAqYHW+Ae4jMU5cqkDU9dJqKYZh7khdB+BGvL9pox8IY3wxfTHsE5+6/cRjM6Tt43pLE9EvraMnHD1mRcrZWyUp; bm_sz=3749B70721DC5D802BD98EE35CC1B89D~YAAQ9NfSF/wqOp5wAQAAoEji9Qd6hEKyMIZzdBHdk/UsA58thkwnGNfGUpz8z7ZnB0pP7ts3pTLowS0o51QigQGdxDwgoCxgTqIbywBkljhHVcMS5YqzJeT4lRth9mQimnP61Rvj4VAaU7xTkMFSVPb2/TIormq2ccnk20ccXCTd8t8dXVu0xZP0l2EX5Byi48k1NSUt0k/b'

root = '/Users/zhaomiao/Desktop/taxi'

# 注意长度限制
reportname = 'CustomerTrave(202002020303)'

imagelist = []

taxiinfo = []

reportresult = []



def run():

    imagelist = getFilelist(root)
    # 以上返回结构
    # [('2.JPG', '/Users/zhaomiao/Desktop/taxi/2.JPG'), ('1.JPG', '/Users/zhaomiao/Desktop/taxi/1.JPG')]

    with open(root + 'taxi.txt', 'w') as file_obj:

        for each in imagelist:
            result = list(getTaxiinfo(each[1]))
            result.append(each[0])
            imageId = str(uploadImage(each[0],each[1]))
            result.append(imageId)
            file_obj.write(str(result) + '\n') # 增加写出到文件步骤，避免反复调用阿里云接口，只有500次免费机会,如有出错图片之后单独处理
            taxiinfo.append(result)
        print(taxiinfo)


    # 以上返回结构
    # [['￥114.00', '2020-01-19', '17:56-19:15', '4.JPG', '2F547E6891863314A32879FA84CFFC03'], ['￥130.00', '2019-12-31', '15:01-16:22', '1.JPG', '3820D108C50235F1AF6F9D1F4AFE4E5D'], ['￥78.00', '2020-01-02', '08:58-09:40', 'IMG_3277.JPG', 'C3956298546B31FBBA0F8511925D6E9E']]

    #Cookies = getIBMCooike() # 登陆cookie信息太少，跳转过多弃用

    reportresult = creReport(reportname)

    time.sleep(10)

    if reportresult[3] == 0:
        '''
        读取taxi文件时需注意，list写出后读回会添加双引号，需要用eval()处理
        '''
        # 调用taxi.txt时弃用
        # with open(root + 'taxi.txt', 'r') as fr:
        #     readitem = fr.read()
        #     taxiinfo = readitem.split('\n')
        for info in taxiinfo: # 如果调用taxi.txt作为taxiinfo，需要将in taxiinfo改为in txt作为taxiinfo[:len(taxiinfo)-1]：
            creItem(reportresult,info) # 如果调用taxi.txt作为taxiinfo，需要将info改成eval(info),
            time.sleep(10)


# 获取出租车票所在文件夹的信息和文件名
def getFilelist(root):
    list = []
    each = []
    for root, dirs, files in os.walk(root, topdown=False):
        for name in files:
            if re.match(r'.+\.JPG$', os.path.join(root, name)):  # 只选取以.JPG结尾的文件
                each = (name,os.path.join(root, name))
                list.append(each)
    print('图像列表获得成功')
    return list

# 通过百度AI识别出租车票，返回TotalFare，Date，Time
def getTaxiinfo(path):


    # 百度出租车票识别率过低，弃用，改为调用阿里云接口，后发现可能是苹果自带软件拍照出的图片问题，在qq软件内拍照可以成功，
    # 使用百度不需要500次的免费限制，每天50

    # 获取百度的access token，每次使用前需要获得，会变
    ApiKey='4dFrsApXlhZDIUEShghapCOv'
    SecretKey='fGxxjTts4RaZFNNttGVkHKfF5WZKyasH'
    url='https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(ApiKey,SecretKey)
    rep=requests.get(url)
    acctoken = rep.json()['access_token']


    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/taxi_receipt"
    # 二进制方式打开图片文件
    f = open(path, 'rb')
    img = base64.b64encode(f.read())

    params = {"image":img,'id_card_side': 'back'}
    access_token = acctoken
    request_url = request_url + "?access_token=" + access_token
    baidu_headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=baidu_headers)
    if response:
        print (path + '的出租车信息获取成功')
        #
    # # 返回结构如下，注意有时附加税扫不出来，结果还是要确认
    # # {'log_id': 8772625137446385296, 'words_result_num': 9, 'words_result': {'Fare': '¥128.60', 'InvoiceNum': '35597977',
    # # 'InvoiceCode': '111001881003', 'FuelOilSurcharge': '¥1.00', 'TotalFare': '¥130.00', 'TaxiNum': 'BT8148', 'Time':
    # # '15:01-16:22', 'Date': '2019-12-31', 'CallServiceSurcharge': '¥0.00'}}
    return taxiinfo['words_result']['TotalFare'],taxiinfo['words_result']['Date'],taxiinfo['words_result']['Time']

    # 阿里的接口复杂，只有500次免费限制，百度识别率满足的情况下，使用百度
    '''
    with open(path, 'rb') as f:
        data = f.read()
        base64_str = str(base64.b64encode(data), 'utf-8')

    dict = {'image': base64_str}

    ssl._create_default_https_context = ssl._create_unverified_context

    ali_headers = {
        'Authorization': 'APPCODE 399fc6098780403ab9c01effd451f557', # 'APPCOD '后有空格不能省，后面的code是阿里云的appcode
        'Content-Type': 'application/json; charset=UTF-8',
        'User-Agent': "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12 "
    }
    url_ali = "https://taxbill.market.alicloudapi.com/api/predict/ocr_taxi"

    taxifare = 0
    taxidate = ''
    taxitime = ''

    try:
        params = json.dumps(dict).encode(encoding='UTF8')
        req = urllib.request.Request(url_ali, params, ali_headers)
        r = urllib.request.urlopen(req)
        # ctx = ssl.create_default_context()
        # ctx.check_hostname = False
        # ctx.verify_mode = ssl.CERT_NONE
        html = r.read()
        r.close();
        taxiresult = json.loads(html.decode("utf8"))
        #位数判断不准确，需要正则表达式
        fare = []
        for each in taxiresult['recipts'][0]['items']:
            if re.search(r"(\d{4}-\d{1,2}-\d{1,2})", each['txt']):
                taxidate = each['txt']
            if re.search(r"(\d{1,2}:\d{1,2}-\d{1,2}:\d{1,2})", each['txt']):
                taxitime = each['txt']
            if '￥' in each['txt']:
                fare.append(each['txt'])
        taxifare = max(fare)
        print(max(fare), taxidate, taxitime)

    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read().decode("utf8"))
    time.sleep(1)

    return taxifare,taxidate,taxitime
    '''

# 获取IBMcookie，后面访问IBM网站时需要的话引用
def getIBMCooike():

    url = 'https://w3id.sso.ibm.com/pkmslogin.form?token=Unknown'
    headers = {}
    headers['User-Agent'] = random.choice(USER_AGENTS)
    data = {}
    data['ogin-form-type'] = 'pwd'
    data['username'] = 'zhmiao@cn.ibm.com'
    data['password'] = 'ibm@@ibmibm@@ibm'

    req = requests.post(url=url, data=data, headers=headers)

    cookie = '; '.join(['='.join(item) for item in req.cookies.items()])
    print('模拟登陆获得cookie完成')
    return cookie

# 上传图片到报销网站，输入为getfilelist获得的信息，输入每个图片对应的imageId，
# 用来与getTaxiinfo获得的出租车信息一起生成item，调用creItem时使用
def uploadImage(imagenm,filepath):

    #生成Content-Type为multipart/form-data类型的数据和header的Content-type
    multipart_encoder = MultipartEncoder(
        fields={
            'file': (
            imagenm, open(filepath, 'rb'), 'image/jpeg'),
        })

    headers['Content-Type'] = multipart_encoder.content_type

    imagereq = requests.post(url=uploadurl, data=multipart_encoder, headers=headers)

    if 'failed' in imagereq.text:
        print(imagereq.text)
        os._exit()
    else:
        if imagereq.text.split('Status: \'')[1][:7] == 'SUCCESS':
            print(imagenm + ' upload successfully')
            imageId = imagereq.text.split(' imageId: \'')[1].split('\', Status:')[0]
        else:
            print(imagenm + ' upload failed')

    time.sleep(10)
    return imageId

# 创建报销report，取得Reportid,RptKey,Name,iscreReportOK，调用creItem时使用
def creReport(reportname):

    rptime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    reportnm = reportname

    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    data = {}
    data['MIME 类型'] = 'application/x-www-form-urlencoded; charset=UTF-8'

    #每次登陆EmpKey会变化
    data['data'] = '[{"action":"ExpenseReport","method":"SaveReport","data":["","N","N","<Report>\n<PolKey>1050</PolKey>\n<FormKey>2567</FormKey>\n<isNew>true</isNew>\n<ApsKey>A_NOTF</ApsKey>\n<PostedSum>0</PostedSum>\n<AllocationFormKey>9</AllocationFormKey>\n<ApvStatusName>未提交</ApvStatusName>\n<AutoPrePopLocation>Y</AutoPrePopLocation>\n<BiHierNodeKey>2932</BiHierNodeKey>\n<ConcurAuditStatus>NOTR</ConcurAuditStatus>\n<CreatedByClientType>ONLINE</CreatedByClientType>\n<CrnKey>34</CrnKey>\n<CtryCode>CN</CtryCode>\n<CrnCode>CNY</CrnCode>\n<CurrencyName>中国，人民币元</CurrencyName>\n<Custom1>2</Custom1>\n<Custom2>GCG</Custom2>\n<Custom4>GTS</Custom4>\n<Custom5>GTS GCG Geo</Custom5>\n<Custom6>GTS GCG Geo</Custom6>\n<Custom8>Y</Custom8>\n<DelegateApproved>N</DelegateApproved>\n<DelegateCreated>N</DelegateCreated>\n<DelegateSubmitted>N</DelegateSubmitted>\n<DispPmtData>N</DispPmtData>\n<EmpKey>' + EmpKey + '</EmpKey>\n<EmpName>null, null</EmpName>\n<EverSentBack>N</EverSentBack>\n<ExceptionApproved>N</ExceptionApproved>\n<FiEnabled>N</FiEnabled>\n<HasNewTravelAllowances>N</HasNewTravelAllowances>\n<ImageRequired>N</ImageRequired>\n<ImageStatus>not.required</ImageStatus>\n<LedgerKey>2001</LedgerKey>\n<LedgerName>SAP Blue Harmony</LedgerName>\n<LimitApproved>N</LimitApproved>\n<Offline>N</Offline>\n<OfflineEdited>N</OfflineEdited>\n<OfflineLocked>N</OfflineLocked>\n<OrgUnit1Name>CN 0684</OrgUnit1Name>\n<OrgUnit1Key>1003168</OrgUnit1Key>\n<OrgUnit1IsDeleted>N</OrgUnit1IsDeleted>\n<OrgUnit1>1003168</OrgUnit1>\n<OrgUnit1Code>CN 0684</OrgUnit1Code>\n<OrgUnit1SyncGuid>5B9B60F84130FF49B9E671836ED8C4F5</OrgUnit1SyncGuid>\n<PayKey>P_NOTP</PayKey>\n<PayStatusName>未付款</PayStatusName>\n<PrepForSubmitEmpKey>N</PrepForSubmitEmpKey>\n<RebuildJournal>N</RebuildJournal>\n<ReceiptImageAvail>N</ReceiptImageAvail>\n<ReceiptRequired>N</ReceiptRequired>\n<ReceiptStatus>不要求</ReceiptStatus>\n<ReceiptsReceived>N</ReceiptsReceived>\n<UserDefinedDate>2020-03-17</UserDefinedDate>\n<WaitingProcessing>N</WaitingProcessing>\n<UserUUID>08ec5060-4ae9-4264-95c0-e4dc7f3c3d65</UserUUID>\n<Name>' + reportname + '</Name>\n<Purpose>Business Travel</Purpose>\n<Custom13>324526</Custom13>\n<Custom13Name>客户相关差旅</Custom13Name>\n<Custom13Code></Custom13Code>\n<OrgUnit4>2</OrgUnit4>\n<OrgUnit4Name>WBS 元素</OrgUnit4Name>\n<OrgUnit4Code></OrgUnit4Code>\n<OrgUnit5>4475787</OrgUnit5>\n<OrgUnit5Name>(C.24HKC.003:Non-billable) C.24HKC.003:Non-billable 3y DCC support for ABC-BJ site</OrgUnit5Name>\n<OrgUnit5Code></OrgUnit5Code>\n<Custom9>N</Custom9>\n<AuthRequests>\n</AuthRequests>\n<CurrentDateTime>' + rptime + '</CurrentDateTime>\n<change>Y</change>\n</Report>","TRAVELER"]}]'

    reportreq = requests.post(url=creReporturl, data=data, headers=headers, verify=False)

    iscreReportOK = 1
    if 'failed' in reportreq.text:
        print(reportreq.text)
        os._exit()
    else:
        if reportreq.text.split('StatusId:"')[1].split('",Report:')[0] == 'SUCCESS!':
            Reportid = reportreq.text.split('ReportId:"')[1].split('",RptKey:')[0]
            RptKey = reportreq.text.split('RptKey:"')[1].split('",RptKeyNoEncr')[0]
            Name = reportreq.text.split('Name:"')[1].split('",Offline:')[0]
            iscreReportOK = 0
            print('Report Created successfully')
        else:
            print('Report Created failed')
            print(reportreq.text)

    return Reportid,RptKey,Name,iscreReportOK

# 使用前面获得的信息，生成每日报销项，注意commet通过时间来判断
def creItem(reportinfo,taxiinfo):

    Comment = ''
    if taxiinfo[2][:2] > '12':
        Comment = 'Go home from ABC'
    else:
        Comment = 'Go to ABC form home'

    imageId = taxiinfo[4]

    Taxidate = taxiinfo[1]

    Cost = taxiinfo[0][1:]

    Reportid = reportinfo[0]
    RptKey  = reportinfo[1]
    Name   = reportinfo[2]

    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'

    data = {}
    data['MIME 类型'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    data['data'] = '[{"action":"ExpenseReport","method":"SaveExpense","data":["<Expense>\n<isNew>true</isNew>\n<ExpKey>TAXIX</ExpKey>\n<FormKey>1257</FormKey>\n<ItemizeStyle>default</ItemizeStyle>\n<IsItemized>N</IsItemized>\n<IsChild>N</IsChild>\n<amtUpdated>true</amtUpdated>\n<reportId>' + Reportid + '</reportId>\n<RptKey>' + RptKey + '</RptKey>\n<ItemizeType>NREQ</ItemizeType>\n<origAllocationAccess>RW</origAllocationAccess>\n<reportEntryTaxFormsLoaded>true</reportEntryTaxFormsLoaded>\n<ExpName>出租车和汽车服务</ExpName>\n<ForeignOrDomestic>HOME</ForeignOrDomestic>\n<HasVat>N</HasVat>\n<ExceptionCount>0</ExceptionCount>\n<ReceiptRequired>N</ReceiptRequired>\n<ReceiptReceived>N</ReceiptReceived>\n<Description>' + Name + '</Description>\n<IsPersonal>N</IsPersonal>\n<IsClearedExceptions>N</IsClearedExceptions>\n<Custom29Name>China</Custom29Name>\n<Custom29Key>174058</Custom29Key>\n<Custom29IsDeleted>N</Custom29IsDeleted>\n<Custom29>174058</Custom29>\n<Custom29Code>CN</Custom29Code>\n<ImageRequired>N</ImageRequired>\n<Custom26>0</Custom26>\n<Custom20Name>China</Custom20Name>\n<Custom20Key>6050</Custom20Key>\n<Custom20IsDeleted>N</Custom20IsDeleted>\n<Custom20>6050</Custom20>\n<Custom20Code>CN</Custom20Code>\n<HasExceptions>N</HasExceptions>\n<Custom18>N</Custom18>\n<HasMobileReceipt>N</HasMobileReceipt>\n<CcLocationResolved>Y</CcLocationResolved>\n<Custom3>CN</Custom3>\n<ExceptionMaxLevel>0</ExceptionMaxLevel>\n<ExchangeRate>1</ExchangeRate>\n<ReceiptType>N</ReceiptType>\n<TravelAllowance>N</TravelAllowance>\n<IsBillable>N</IsBillable>\n<HasTimestamp>N</HasTimestamp>\n<AllocationState>N</AllocationState>\n<ClaimedAmount>0</ClaimedAmount>\n<ExchangeRateDirection>M</ExchangeRateDirection>\n<FormType>EXP</FormType>\n<PostedCrnCode>CNY</PostedCrnCode>\n<FormSignature>1257_TRAVELER_P1050_ADJAMT_HD</FormSignature>\n<AttendeeCount>0</AttendeeCount>\n<HasAttendees>N</HasAttendees>\n<itemizeRefresh>Y</itemizeRefresh>\n<ReceiptImageId>' + imageId + '</ReceiptImageId>\n<ExpNameCode></ExpNameCode>\n<Custom21>6149</Custom21>\n<Custom21Name>出租车 (TX)</Custom21Name>\n<Custom21Code></Custom21Code>\n<TransactionDate>' + Taxidate + '</TransactionDate>\n<VendorDescription>Beijing taxi</VendorDescription>\n<LnKey>4180</LnKey>\n<LocName>Beijing, Beijing (北京)</LocName>\n<LocNameCode></LocNameCode>\n<PatKey>CASH</PatKey>\n<TransactionAmount>' + Cost + '</TransactionAmount>\n<PostedAmount>' + Cost + '</PostedAmount>\n<Comment>' + Comment + '</Comment>\n<CrnCode>CNY</CrnCode>\n<PatName>现金</PatName>\n<change>Y</change>\n</Expense>","TRAVELER","<MRU>\n<MruListId>mru_expensetype,1050</MruListId>\n<Value>TAXIX</Value>\n</MRU><MRU>\n<MruListId>mru_locationpicker</MruListId>\n<Value>4180</Value>\n</MRU><MRU>\n<MruListId>mru_ENTRYINFO_1102</MruListId>\n<Value>6149</Value>\n</MRU>","","",""]}]'

    itemreq = requests.post(url=creItemrul, data=data, headers=headers, verify=False)

    if itemreq:
        print(Taxidate + 'create successfully')
    else:
        print(Taxidate + 'create failed')

if __name__ == "__main__":
    run()



