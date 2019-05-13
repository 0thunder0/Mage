#coding:utf-8
import time,random,urllib,os
from pyquery import PyQuery as pq
from selenium import webdriver
#from pyvirtualdisplay import Display
#display=Display(visible=0,size=(800,800))
#display.start()
driver=webdriver.Firefox()
driver.get('https://weibo.com/login.php')
time.sleep(random.randint(10,25))
#登录微博
driver.find_element_by_id('loginname').clear()
driver.find_element_by_id('loginname').send_keys('13276710110')
driver.find_element_by_name('password').send_keys('0thunder0')
#driver.find_element_by_link_text('<span node-type="submitStates"">登录</span>').click()
driver.find_element_by_xpath('//div[@id="pl_login_form"]//div[@class="info_list login_btn"]/a').click()
time.sleep(random.randint(5,15))

#读取微博网址列表
weibo_url_list=[]
with open('weibo_url.txt','r+') as f:
    for url in f:
        weibo_url_list.append(url.replace('\n',''))
print(weibo_url_list)
#批量打开微博网址
for url in weibo_url_list:
    js='window.open'+'("'+url+'")'
    driver.execute_script(js)
    time.sleep(random.randint(5,10))
#判断当前页是否是是否是需要的页面
xyz=1
window_1=driver.current_window_handle
handles=driver.window_handles
for current_handle in handles:
#    if current_handle != window_1:
#        driver.switch_to.window(current_handle)
    if xyz==1:
        xyz=xyz+1
        driver.close()
        continue
    driver.switch_to.window(current_handle)
    print(driver.title)
    driver.close()
#driver.get_screenshot_as_file('weibo_screenshot.png')
driver.quit()
#display.stop()
