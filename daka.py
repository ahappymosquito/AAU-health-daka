import requests
from lxml import etree
import json

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options

ll = [
    ['21115288','464564','xuwenchao','1653828989@qq.com','河南省','焦作市','山阳区','410800']
    ]

def getCookie(user,pw,chrome_options):
    wd = webdriver.Chrome(chrome_options=chrome_options, executable_path='/opt/google/chrome/chromedriver') #Chrome驱动的位置，此学习记录中安装到了Chrome程序根目录，该路径为绝对路径
    # wd= webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')
    # driver.find_element(by=By.ID, value='toolbar-search-input').send_keys('python')
    wd.get('http://fresh.ahau.edu.cn/yxxt-v5/web/xsLogin/login.zf?rdt=web%2Fjkxxtb%2FtbJkxx')
    wd.find_element(by=By.ID,value='zh').send_keys(user)
    wd.find_element(by=By.ID,value='mm').send_keys(pw)
    wd.find_element(by=By.ID,value='dlan').click()
    # time.sleep(2)
    # wd.swich_to_alert().accept()
    cookie=wd.get_cookies()[0]['value']
    wd.quit()
    return cookie

def getInfo(cookie,sheng,shi,qu,code):
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'JSESSIONID='+cookie,
    'Host': 'fresh.ahau.edu.cn',
    'Pragma': 'no-cache',
    'Referer': 'http://fresh.ahau.edu.cn/yxxt-v5/web/xsLogin/login.zf?rdt=web%2Fjkxxtb%2FtbJkxx',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49'
    }
    response=requests.get("http://fresh.ahau.edu.cn/yxxt-v5/web/jkxxtb/tbJkxx.zf",headers=headers)
    # print(response.text)
    htmlele=etree.HTML(response.text)
    #time.sleep(1)
    xh=htmlele.xpath('//*[@id="xh"]/@value')[0]
    xm=htmlele.xpath('//*[@id="xm"]/@value')[0]
    sjdks=htmlele.xpath('//*[@id="sjdks"]/@value')[0] 
    sjdjs=htmlele.xpath('//*[@id="sjdjs"]/@value')[0]
    tbsj=htmlele.xpath('//*[@id="tbsj"]/@value')[0]
    jlid=htmlele.xpath('//*[@id="jlid"]/@value')[0]
    dqrq=htmlele.xpath('//*[@id="dqrq"]/@value')[0]
    sjdbz=htmlele.xpath('//*[@id="sjdbz"]/@value')[0]
    # time.sleep(1)
    postdata={'xh':xh,
    'xm':xm,
    'sjdks':sjdks,
    'sjdjs':sjdjs,
    'tbsj':tbsj,
    'jlid':jlid,
    'tbzt':'0',
    'dqrq':dqrq,
    'sjdfgbz':'全天',
    'sjdbz':dqrq,
    'tw':'37.0',
    'tmda1':'否',
    'tmda2':'否',
    'dqszdmc':sheng+shi+qu,
    'tmda6':'',
    'bz':'健康',
    'ydqszsfmc':sheng,
    'ydqszsmc':shi,
    'ydqszxmc':qu,
    'dqszddm':code
    }
    return postdata

def post(data):
    headersbc = {
    'Host': 'fresh.ahau.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://fresh.ahau.edu.cn/yxxt-v5/web/jkxxtb/tbJkxx.zf',
    'Content-Length': '525',
    'Origin': 'http://fresh.ahau.edu.cn',
    'DNT': '1',
    'Connection': 'keep-alive',
    #'Cookie': 'JSESSIONID=DE31F01B2DC2326D157B9327BB65381C',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
    }
    # requests.post("http://fresh.ahau.edu.cn/yxxt-v5/web/jkxxtb/tbBcJkxx.zf",headers=headersbc,data=postdata)
    # time.sleep(60)
    res = requests.post("http://fresh.ahau.edu.cn/yxxt-v5/web/jkxxtb/tbBcJkxx.zf",headers = headersbc,data = data)
    #print(res.text)
    # print(postdata)
    json1 = json.loads(res.text)
    # print(json1)
    return json1

def inlog(name,postdata,msg):
    with open("/daka/data/"+name+".txt",'a') as f:
        if msg['message']=='保存数据成功':
            f.write(postdata['tbsj']+'今日你已完成打卡'+'<br>')
        #+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

def sendMail(mail,name):
    if mail != '':
        my_sender='ne0_xu@163.com'    # 发件人邮箱账号
        my_pass = ''              # 发件人邮箱密码
        my_user=mail      # 收件人邮箱账号
        def mail():
            ret=True
            try:
                datalog = open("/daka/data/"+name+".txt")
                msg=MIMEText(datalog.read(),'plain','utf-8')
                msg['From']=formataddr(["ahappymosquito",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
                msg['To']=formataddr([name,my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
                msg['Subject']="安徽农业大学健康打卡(已改为安全打卡)"                # 邮件的主题，也可以说是标题
        
                server=smtplib.SMTP_SSL("smtp.163.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
                server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
                server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
                server.quit()  # 关闭连接
            except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
                ret=False
            return ret

        ret=mail()
        if ret:
            print(name+"邮件发送成功")
        else:
            print("邮件发送失败")

if __name__ ==  '__main__':
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox') #让Chrome在root权限运行
    chrome_options.add_argument('--disable-dev-shm-usage') #不打开图形界面
    chrome_options.add_argument('--headless') #浏览器不提供可视化页面
    chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
    chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug

    for user,pw,name,mail,sheng,shi,qu,code in ll:
        # 获取cookie
        try:
            cookie = getCookie(user,pw,chrome_options)
        except IndexError:
            print ("error")
            time.sleep(10)
            cookie = getCookie(user,pw,chrome_options)

        # get信息
        postdata = getInfo(cookie,sheng,shi,qu,code)

        # post请求
        msg = post(postdata)
        #print(msg)

    # 休眠3分钟 等待服务器响应
    time.sleep(20)

    for user,pw,name,mail,sheng,shi,qu,code in ll:
        # 获取cookie
        try:
            cookie = getCookie(user,pw,chrome_options)
        except IndexError:
            print ("error")
            time.sleep(10)
            cookie = getCookie(user,pw,chrome_options)

        # get信息
        postdata = getInfo(cookie,sheng,shi,qu,code)

        # post请求
        msg = post(postdata)
        print(msg)

        # 写入文件
        inlog(name,postdata,msg)

        #发送邮件
        sendMail(mail,name)





