import requests
from lxml import etree
import json

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

wd = webdriver.Chrome(chrome_options=chrome_options, executable_path='/opt/google/chrome/chromedriver') #Chrome驱动的位置，此学习记录中安装到了Chrome程序根目录，该路径为绝对路径



# wd= webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')
# driver.find_element(by=By.ID, value='toolbar-search-input').send_keys('python')
wd.get('http://fresh.ahau.edu.cn/yxxt-v5/web/xsLogin/login.zf?rdt=web%2Fjkxxtb%2FtbJkxx')

user='21115288'
pw='036513'

wd.find_element(by=By.ID,value='zh').send_keys(user)
wd.find_element(by=By.ID,value='mm').send_keys(pw)
wd.find_element(by=By.ID,value='dlan').click()
#time.sleep(2)
#wd.swich_to_alert().accept()

cookie=wd.get_cookies()[0]['value']

wd.quit()




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

print(response.text)

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
time.sleep(1)

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
'tw':'36.5',
'dqszdmc':'安徽省合肥市蜀山区',
'tmda6':'',
'bz':'健康',
'ydqszsfmc':'安徽省',
'ydqszsmc':'合肥市',
'ydqszxmc':'蜀山区',
'dqszddm':'340100'
}

res =requests.post("http://fresh.ahau.edu.cn/yxxt-v5/web/jkxxtb/tbBcJkxx.zf",headers=headersbc,data=postdata)
print(res.text)
# print(postdata)
json1 = json.loads(res.text)

f=open("log.txt",'a')
f.write('打卡时间：'+postdata['tbsj']+json1['message']+','+'现在时间是'+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())+'\n')
f.close()



