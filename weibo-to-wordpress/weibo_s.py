#coding:utf-8
import time,random,urllib,os
from urllib import error
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from pyvirtualdisplay import Display
#display=Display(visible=0,size=(800,800))
#display.start()

driver=webdriver.Firefox()
driver.get('https://passport.weibo.cn/signin/login')
time.sleep(random.randint(10,25))
#登录微博
driver.find_element_by_id('loginName').clear()
driver.find_element_by_id('loginName').send_keys('13276710110')
driver.find_element_by_id('loginPassword').send_keys('@ye13276710110')
#driver.find_element_by_link_text('<span node-type="submitStates"">登录</span>').click()
driver.find_element_by_id('loginAction').click()
time.sleep(random.randint(5,15))

#读取微博网址列表
weibo_url_list=[]
with open('weibo_url.txt','r+') as f:
    for url in f:
        weibo_url_list.append(url.replace('\n',''))
#批量打开微博网址
for url in weibo_url_list:
    js='window.open'+'("'+url+'")'
    driver.execute_script(js)
    time.sleep(random.randint(5,15))
#判断当前页是否是是否是需要的页面
xyz=1
handles=driver.window_handles
window_1=driver.current_window_handle
for current_handle in handles:
    #if current_handle != window_1:
    #    driver.switch_to.window(current_handle)
    if xyz==1:
        xyz=xyz+1
        driver.close()
        continue
    driver.switch_to.window(current_handle)
    #print(driver.title)
    time.sleep(random.randint(10,25))
    try:
        driver.find_element_by_xpath('//div[@id="Pl_Official_Nav__2"]//td[2]/a').click()
    except:
        continue
#用js控制下拉
    js='document.documentElement.scrollTop=9000'
    num=1
    for i in range(1,70):
        #driver.execute_script(js)
        driver.find_element_by_css_selector('body').send_keys(Keys.END)
        time.sleep(random.randint(2,7))
        print('开始下拉%s次' %num)
        num=num+1
    page_source=driver.page_source
    data=pq(page_source)
#获取博客标题作为文件夹名称
    title=driver.title
    wb_title=title.split('的')[0]
    fpath=os.getcwd()+'/'+wb_title
#创建文件夹
    if os.path.exists(fpath) is False:
        os.makedirs(fpath)
#下载图片
    img_download_urls=[]
    img_urls=data('.photo_module .photo_cont a img').items()
    for img_cache in img_urls:
        img_url=img_cache.attr('src').split('?')[0].split('/')[-1]
        new_img_url='https://wx2.sinaimg.cn/large/'+img_url
        img_download_urls.append(new_img_url)
    n=1
    for imgUrl in img_download_urls:
        img_download_path=fpath+'/'+imgUrl.split('/')[-1]
        try:
            print('正在下载图片%s/%s：' %(n,len(img_download_urls)),imgUrl)
            urllib.request.urlretrieve(imgUrl,img_download_path)
        except :
            continue
        n=n+1
    time.sleep(random.randint(8,15))
    driver.close()
#driver.get_screenshot_as_file('weibo_screenshot.png')
driver.quit()
#display.stop()
