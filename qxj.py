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

chrome_options = Options()
chrome_options.add_argument('--no-sandbox') #让Chrome在root权限运行
chrome_options.add_argument('--disable-dev-shm-usage') #不打开图形界面
chrome_options.add_argument('--headless') #浏览器不提供可视化页面
chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug

ll = [
]

for user,pw,name,mail in ll:

    # 获取cookie
    wd = webdriver.Chrome(chrome_options=chrome_options, executable_path='/opt/google/chrome/chromedriver') #Chrome驱动的位置，此学习记录中安装到了Chrome程序根目录，该路径为绝对路径
    # wd= webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')
    # driver.find_element(by=By.ID, value='toolbar-search-input').send_keys('python')
    wd.get('http://fresh.ahau.edu.cn/yxxt-v5/web/xsLogin/login.zf')
    wd.find_element(by=By.ID,value='zh').send_keys(user)
    wd.find_element(by=By.ID,value='mm').send_keys(pw)
    wd.find_element(by=By.ID,value='dlan').click()
    #time.sleep(2)
    #wd.swich_to_alert().accept()
    cookie=wd.get_cookies()[0]['value']
    wd.quit()

    headers={
    'Host': 'fresh.ahau.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Length': '201',
    'Origin': 'http://fresh.ahau.edu.cn',
    'Connection': 'keep-alive',
    'Referer': 'http://fresh.ahau.edu.cn/yxxt-v5/qj/xsqj/cx.zf',
    'Cookie': 'JSESSIONID='+ cookie
    }


    data = {
        'lx':	"5",
        'autocomplete':	"",
        'sc':	"北三门往返",
        'kssj':	"2022-10-07 06:00:00",
        'jssj':	"2022-10-07 23:10:00",
        'nr':	"合肥市内当天返回"
    }
    res = requests.post("http://fresh.ahau.edu.cn/yxxt-v5/qj/xsqj/zjbc.zf",headers=headers,data=data)
    print(res.text)
