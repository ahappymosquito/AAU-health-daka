import requests
from lxml import etree
import json
import base64
import time

from PyRsa.pyrsa import RsaKey
from PyRsa.pyb64 import Base64
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
# from selenium.webdriver.common.keys import Keys

# wd= webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')
# # driver.find_element(by=By.ID, value='toolbar-search-input').send_keys('python')
# wd.get('http://fresh.ahau.edu.cn/yxxt-v5/web/xsLogin/login.zf?rdt=web%2Fjkxxtb%2FtbJkxx')

# user='21115288'
# pw='036513'

# wd.find_element(by=By.ID,value='zh').send_keys(user)
# wd.find_element(by=By.ID,value='mm').send_keys(pw)
# wd.find_element(by=By.ID,value='dlan').click()
# #time.sleep(2)
# #wd.swich_to_alert().accept()

# cookie=wd.get_cookies()[0]['value']

# wd.quit()



getPublicKeyUrl = 'http://fresh.ahau.edu.cn/yxxt-v5/xtgl/login/getPublicKey.zf'  # 获取公钥
loginUrl = 'http://fresh.ahau.edu.cn/yxxt-v5/web/xsLogin/Login.zf'  # 登录
#           http://fresh.ahau.edu.cn/yxxt-v5/web/xsLogin/login.zf
checkurl = 'http://fresh.ahau.edu.cn/yxxt-v5/web/xsLogin/checkLogin.zf'
zhlx='xsxh'
zh= ''
mm=''

headers = {'Host': 'fresh.ahau.edu.cn',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
           'Accept-Encoding': 'gzip, deflate',
           'Connection': 'keep-alive',
           'Upgrade-Insecure-Requests': '1',
           'Pragma': 'no-cache',
           'Cache-Control': 'no-cache'}


cookie = requests.get(loginUrl,headers=headers).cookies['JSESSIONID']
print(cookie)

headers1 = {
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


# time.sleep(30)
mes = requests.get(getPublicKeyUrl).json()
# print(mes['modulus'])
rsakey = RsaKey()
rsakey.set_public(Base64().b64tohex(mes['modulus']), Base64().b64tohex(mes['exponent']))

enPassword = Base64().hex2b64(rsakey.rsa_encrypt(mm))
enZh = Base64().hex2b64(rsakey.rsa_encrypt(zh))
enZhlx = Base64().hex2b64(rsakey.rsa_encrypt(zhlx))
dldata = base64.b64encode(json.dumps({"zhlx": enZhlx, "zh": enZh, "mm": enPassword}).replace(' ', '').encode("utf-8")).decode('utf-8')
print(dldata)

state = requests.post(checkurl,headers=headers1,data=dldata)
print(state.text)

# eyJ6aGx4IjoiUHdGc3BmRzhNMkYyak5hMzNCcTNrU0NjcnN1d2NXT3dyc3JVajM3OFh6VzVSWEZBalppcHJ5eFhkRnBGa0Urblc1b1A3VlJpUWJDVCtzYTZHRmVOaXdIbzVLNEwzb0l1SS9qUXFaMnVucEhWSDJrQjUzMjk2REdpUEtVTEJKN3BDVFgxQXBsNkZ0NEVyQkdWU0lSd1BtV0N0NFRWOWtGYWEzcHJ3Q0F0U1Y0PSIsInpoIjoia3JwdmRhYzd0ckwrQis2MFJVUUV2OENOZWFFR1FIcDQ1OGo0dTZqRGdKNU1UL3h0RXpoVlZnZlF4YlZXcVFvNm44M0NVbUpVZTI2eWpGaEhUZmdtcVczU3ZwTnNLMGNHUzk4YmlXc2x3TGlHc0VtSFZ5T2RVUjh3WmhTbEZSRno5bXZCQTd0QldOaVJ3U3RtUlcwSDRyWTlrWWtGNi9DOVBYbkRTWVVkZVZFPSIsIm1tIjoia3U4Z0tjdHVnM0IvNGVSQnBzV0kxS0lqVTRValRKbldVMldHTVBzTzR3NEpSbW1GdmxXOVhaTTF6ZnRXclg1U1hqWHJhanI4MHhjVE94andBQVBxTk1taUsrTFQ4aHQvSUxjMmtlRHpaQTd3T0d0emltUFEyQXdvanVqNjBZdy95TmJsSTZmL1VuZlZkL0pIZTlRdmRmek9NbUg4Ti81eXNJeGhGSWM1VGc4PSJ9




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
print(postdata)



