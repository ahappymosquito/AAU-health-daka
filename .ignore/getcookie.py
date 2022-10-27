from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys

wd= webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')
# driver.find_element(by=By.ID, value='toolbar-search-input').send_keys('python')
wd.get('http://fresh.ahau.edu.cn/yxxt-v5/web/xsLogin/login.zf?rdt=web%2Fjkxxtb%2FtbJkxx')

user='21115245'
pw='023010'

wd.find_element(by=By.ID,value='zh').send_keys(user)
wd.find_element(by=By.ID,value='mm').send_keys(pw)
wd.find_element(by=By.ID,value='dlan').click()
#time.sleep(2)
#wd.swich_to_alert().accept()

cookie=wd.get_cookies()[0]['value']

time.sleep(3)
wd.quit()