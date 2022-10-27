import random
import time
import requests
import json
from pyquery import PyQuery as pq
from PyRsa.pyrsa import RsaKey
from PyRsa.pyb64 import Base64


def is_useful_jsessionid(jsessionid, bigipserver):
    """
    此函数用来测试获取到的 JSESSIONID 是否可用
    :param jsessionid: 
    :param bigipserver: 
    :return: 
    """
    kb_url = 'http://{self.domain}/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N253508'
    kb_headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Content-Length': '14',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Cookie': f'JSESSIONID={jsessionid}; BIGipServerjwxtnew_BS80={bigipserver}',
        'Host': '{self.domain}',
        'Origin': 'http://{self.domain}',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://{self.domain}/jwglxt/kbcx/xskbcx_cxXskbcxIndex.html?gnmkdm=N253508'
                   '&layout=default&su=201730615063',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/76.0.3809.87 Safari/537.36', 'X-Requested-With': 'XMLHttpRequest'
    }
    data = {
        'xnm': 2019,
        'xqm': 3
    }
    res = requests.post(kb_url, headers=kb_headers, data=data)
    if res.status_code == 200:
        return True
    return False


class TimeTable:
    def __init__(self, yhm, mm):
        self.yhm = yhm
        self.mm = mm
        self.session = requests.Session()
        self.raw_cookie = {}
        self.domain = 'xxx.com'  ## 换成使用新版正方教务的学校域名

    def get_raw_cookies_csrf(self):
        headers = {
            'Host': f'{self.domain}',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/76.0.3809.87 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;'
                      'q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }
        url = f'http://{self.domain}/jwglxt/xtgl/login_slogin.html'
        res = self.session.get(url, headers=headers)
        doc = pq(res.text)
        self.csrf = doc('#csrftoken').attr('value')
        self.raw_cookie = requests.utils.dict_from_cookiejar(res.cookies)
        # print('JSESSIONID', self.raw_cookie['JSESSIONID'])
        # print('BIGipServerjwxtnew_BS80', self.raw_cookie['BIGipServerjwxtnew_BS80'])

    def get_json(self):
        self.getpublickey_t = int(time.time() * 1000)
        url = f'http://{self.domain}/jwglxt/xtgl/login_getPublicKey.html?time={self.getpublickey_t}'
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': f'JSESSIONID={self.raw_cookie["JSESSIONID"]};'
                      f' BIGipServerjwxtnew_BS80={self.raw_cookie["BIGipServerjwxtnew_BS80"]}',
            'Host': f'{self.domain}',
            'Referer': f'http://{self.domain}/jwglxt/xtgl/login_slogin.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/76.0.3809.87 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        try:
            res = self.session.get(url, headers=headers)
            rj = res.json()
            return rj['modulus'], rj['exponent']
        except:
            print('Fail')

    def get_jsessionid(self):
        # csrf = self.get_csrf()
        rsakey = RsaKey()
        m, e = self.get_json()
        rsakey.set_public(Base64().b64tohex(m), Base64().b64tohex(e))
        rr = rsakey.rsa_encrypt(self.mm)
        enpsw = Base64().hex2b64(rr)
        # print('csrf:', self.csrf)
        # print('mm:', enpsw)
        data = {
            'csrftoken': self.csrf,
            'yhm': self.yhm,
            'mm': enpsw
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;'
                      'q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '470',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': f'JSESSIONID={self.raw_cookie["JSESSIONID"]}; '
                      f'BIGipServerjwxtnew_BS80={self.raw_cookie["BIGipServerjwxtnew_BS80"]}',
            'Host': f'{self.domain}',
            'Origin': f'http://{self.domain}',
            'Referer': f'http://{self.domain}/jwglxt/xtgl/login_slogin.html',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/76.0.3809.87 Safari/537.36'
        }
        dt = random.randint(5, 10)
        url = f'http://{self.domain}/jwglxt/xtgl/login_slogin.html?time={self.getpublickey_t - dt}'
        # print(self.getpublickey_t - dt)
        res = self.session.post(url, headers=headers, data=data)
        if len(res.history) and res.history[0].status_code == 302:
            js = requests.utils.dict_from_cookiejar(res.history[0].cookies)
            ll = self.parser(js['JSESSIONID'])
            print(ll)
        else:
            print('Fail to get courses')

    def parser(self, js):
        """
        解析教务处，取出课程表数据
        :return:
        """
        url = f'http://{self.domain}/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N253508'
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '23',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie': f'JSESSIONID={js}; '
                      f'BIGipServerjwxtnew_BS80={self.raw_cookie["BIGipServerjwxtnew_BS80"]}',
            'Host': f'{self.domain}',
            'Origin': f'http://{self.domain}',
            'Referer': f'http://{self.domain}/jwglxt/kbcx/xskbcx_cxXskbcxIndex.html'
                       '?gnmkdm=N253508&layout=default&su=201864730502',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/76.0.3809.87 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        from_data = {
            'xnm': '2019',
            'xqm': '3'
        }

        resp = self.session.post(url, headers=headers, data=from_data)
        if resp.status_code == 200:
            res = resp.text
            # print(json.loads(res)['kbList'])
            courses = []
            courses_d = {}
            for course in json.loads(res)['kbList']:
                courses_d['location'] = course['cdmc']
                if len(self._section2list(course['jcs'])):
                    courses_d['startTime'] = self._section2list(course['jcs'])[0]
                    courses_d['endTime'] = self._section2list(course['jcs'])[-1]
                courses_d['name'] = course['kcmc']
                # courses_d['point'] = course['xf']
                courses_d['teacher'] = course['xm']
                courses_d['day'] = course['xqj']
                courses_d['weeks'] = self._weeks2list(course['zcd'])
                courses.append(courses_d)
                courses_d = {}
            return self.tran2everyday(courses)
        else:
            print('Fail to get courses!')

    def _section2list(self, s='3-4'):
        """
        将节数转为数组
        :param s:
        :return:
        """
        sections = []
        if '-' in s:
            sections += [i for i in range(int(s.split('-')[0]), int(s.split('-')[1]) + 1)]
        return sections

    def _weeks2list(self, s='1-11周,14周'):
        """
        将周数转为数组
        :param s:
        :return:
        """
        weeks = []
        for week in s.replace(',', '').split('周')[:-1]:
            if '-' in week:
                weeks += [i for i in range(int(week.split('-')[0]), int(week.split('-')[1]) + 1)]
            else:
                weeks.append(int(week))
        return weeks

    def operator(self):
        self.get_raw_cookies_csrf()
        self.get_jsessionid()


if __name__ == '__main__':
    tt = TimeTable('2017xxxxxxxx', '1234567890')
    tt.operator()
