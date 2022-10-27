import random
import requests
from lxml import etree
import json
import base64
import time

from PyRsa.pyrsa import RsaKey
from PyRsa.pyb64 import Base64


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
# print(dldata)

state = requests.post(checkurl,headers=headers1,data=dldata)
print(state)



# eyJ6aGx4IjoiWTdaMW42R29ockhyaFk5NVFCRERhVXE4ajBmWVRkU1VwTGRHSWowenk0UTRlRHNOYll1RVpXK0U1ZC9mMUd5RDVodFovNStwZmhVSE5zb01PQmFncXdsdW9XQ1pzalMwNUdwU1RKS2gxTkVDYWlld2xraytISUxXaTN2bzEvdEFaRjBrcDZkcjhxZ3BqbWlaa1NKUnAvejVqWFplalZrLytTajRQTnBDWC9jPSIsInpoIjoiYXJTSE1zVjVHQ2NDTTV0bk9ZRTFJWDQ4dFBScUwxS2hmai9FdVFYR2dhc1o5ZTNrWVRoNzZVZlhVOVdBREgxK01XQjA1U2tYRk1kOHBCUGVqU0pZV1lYWjBzTmhOdi92UDFKM09Ia0twUkVQVkJRVFdYNC9jT1RIeGlPNmMvZWlQY3h6MzN2SitXVnV6Y1duOElkUlRwb1RpdjAwV2l4R2s2WktjdUo2b3F3PSIsIm1tIjoiQXhkcUhKTVEyZFlYK1puZU90dVNyTWl1cm4veG5YSW1ZWHI1TGhwVy9mZlMyUENaTjkwdXBEWE8vRTNpTFBQSW9DZ3JiWS9LZ0pKTXJzYXMwNGU2cHhUZzVWcFo4bjZGWVdPWGFRZUd5OGhCNEhzV0JBS3c0S1Qxdy9FejZFSFpwVWFaNGIyZmtja0lacVRZQ0VhbjU4cjJNaTFNNnpyUHJ5bEdzRVpCdjdnPSJ9
# eyJ6aGx4IjoiS1BiRXp0ZlQ0TXFldm1wUWtFRW0vdkh5UUJmbWU1QjlybEM2eEIwUHVXR3g4UTZTcHZjbmVRamFDM05nWlI4eG9tVDM4LzBNOXFvWmNEMElqN2tkYkJNZ0Q1T0g2enFGQWZGUC9PdmhSd29kaXVDMFNIN2xkRjdvTHFQeXAzM2JyZGx6bGNQbnlsd3RIYmJwejA4cytBa1hVV0NqZExMRm9BMnJaV2FuSjFjPSIsInpoIjoiZ0dPRHp5elc3eVVXakR3Vkx5c00zRlhMVGNsTFBVMlhOVzRFWWpXc1lzTithSkpIY2t4a0tQQnFxWlBFdjMvMVE5eWU0TEpEWlZETVRPdHdDSnlYRXRjekdoaDhsRVNsa2EydTBEdXBqcmhjN3gxZ2NDSmlUSzExanJyUVE1eXlvdHJaa2tmWm51emhXNTBJYnZmTnZoa3FGbkNDTFlOOWVWaTc3VHo0RnZnPSIsIm1tIjoiZ1ZrVUp4SWxUZmlZVkpFUTZHQXJNbzN0WThNSXZkVm9jcVFUdzh4TGRMQlJDOVVCYzRyczM0K1VsNG5hT2hBeTQ2ajlvRGxCa253TGpremlENkxHczEwK3JZOU9MQTJjNVJSazR6OXJCMG5nY0FXdHkwVlgySTFYY09WSUFMelhxMkhQcVp0V3NZRktaaFJpdGFzNUMwZlk0WWVmSit0clZPSEdDZTVRMVdrPSJ9

# modulus = "AJftLhHzsQPu1LwCgOR41hRKn4tbaD/ehyZKiBWDYCpaualtMyJIT0SzBl07O2NwjxI8uwr82SMvEW9iiSEoBylHOWNnEzyOYwXb29xMo+D4LTVqMX7NkAliIqH+wOSA1g0DVxmcQWCtGVI4vDUnGIN8tYPlxc9NIXN5zO0HwqKn"
# exponent = "AQAB"
# rsakey.set_public(Base64().b64tohex(modulus), Base64().b64tohex(exponent))
# psw = "1234567890"
# en_psw = Base64().hex2b64(rsakey.encrypt(pre_psw))


# def get_raw_cookies_csrf(self):
#     headers = {
#         'Host': f'{self.domain}',
#         'Connection': 'keep-alive',
#         'Upgrade-Insecure-Requests': '1',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                       'Chrome/76.0.3809.87 Safari/537.36',
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;'
#                   'q=0.8,application/signed-exchange;v=b3',
#         'Accept-Encoding': 'gzip, deflate',
#         'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
#     }
#     url = f'http://{self.domain}/jwglxt/xtgl/login_slogin.html'
#     res = self.session.get(url, headers=headers)
#     doc = pq(res.text)
#     self.csrf = doc('#csrftoken').attr('value')
#     self.raw_cookie = requests.utils.dict_from_cookiejar(res.cookies)



#     def get_jsessionid(self):
#         rsakey = RsaKey()
#         m, e = self.get_json()
#         rsakey.set_public(Base64().b64tohex(m), Base64().b64tohex(e))
#         rr = rsakey.rsa_encrypt(self.mm)
#         enpsw = Base64().hex2b64(rr)
#         # print('csrf:', self.csrf)
#         # print('mm:', enpsw)
#         data = {
#             'csrftoken': self.csrf,
#             'yhm': self.yhm,
#             'mm': enpsw
#         }
#         headers = {
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;'
#                       'q=0.8,application/signed-exchange;v=b3',
#             'Accept-Encoding': 'gzip, deflate',
#             'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
#             'Cache-Control': 'max-age=0',
#             'Connection': 'keep-alive',
#             'Content-Length': '470',
#             'Content-Type': 'application/x-www-form-urlencoded',
#             'Cookie': f'JSESSIONID={self.raw_cookie["JSESSIONID"]}; '
#                       f'BIGipServerjwxtnew_BS80={self.raw_cookie["BIGipServerjwxtnew_BS80"]}',
#             'Host': f'{self.domain}',
#             'Origin': f'http://{self.domain}',
#             'Referer': f'http://{self.domain}/jwglxt/xtgl/login_slogin.html',
#             'Upgrade-Insecure-Requests': '1',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                           'Chrome/76.0.3809.87 Safari/537.36'
#         }
#         dt = random.randint(5, 10)
#         # dt 的作用实际上是尽可能模拟浏览器，浏览器上获取公钥页相对于此页面有些许延迟，事实上不减去 dt 也能正常运行
#         url = f'http://{self.domain}/jwglxt/xtgl/login_slogin.html?time={self.getpublickey_t - dt}'
#         # print(self.getpublickey_t - dt)
#         res = self.session.post(url, headers=headers, data=data)
#         if len(res.history) and res.history[0].status_code == 302:
#             js = requests.utils.dict_from_cookiejar(res.history[0].cookies)
#             return js['JSESSIONID']
#         else:
#             print('Fail to get JSESSIONID！')