from wp_plugin import wp_plugin 
import time,random,os,urllib
from pyquery import PyQuery as pq
urls=['http://www.hizbo.com/meinv/']
#header={"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"}
header={'User-Agent':'Opera/9.80(Macintosh;IntelMacOSX10.6.8;U;en)Presto/2.8.131Version/11.11'}
def urls_collect(url):
    req=urllib.request.Request(url,headers=header)
    data = urllib.request.urlopen(req).read()
    page_source=pq(data)

    if not os.path.isfile('novel.txt'):
        os.mknod('novel.txt')
    with open('novel.txt','r+') as f:
        novelCache=f.readlines()
    for i in range(len(novelCache)):
        novelCache[i]=novelCache[i].replace('\n','')
    #采集所有文章链接
    novel_list=[]
    urls=page_source('.listmain dd').items()
    
    for ur in urls:
        url_cache=ur('a').attr('href')
        if url_cache not in novelCache:
            novel_list.append(url_cache)
    #给文章链接排序
    list_cache=[]
    list_cache.append(novel_list[0])
    if len(novel_list) == 0:
        return None
    else:
        for i in range(len(novel_list)):
            no_1=novel_list[i].split('.')[0]
            no_2=list_cache[-1].split('.')[0]
            if no_1 < no_2:
                list_cache[-1]=novel_list[i]
            elif no_1== no_2:
                continue
            else:
                list_cache.append(novel_list[i])
        return list_cache

def parse_post(main_url,post_urls):
    with open('novel.txt','a+') as f:
        for url in post_urls:
            f.writelines(url+'\n')
            r_url=main_url+url
            #print(r_url)
            req=urllib.request.Request(r_url,headers=header)
            data = urllib.request.urlopen(req).read()
            data=pq(data)
            title=data('.content h1').text()
            content=data('#content').text()            
            yield title,content

if __name__=='__main__':

    login_url='http://if.fyi/xmlrpc.php'
    login_user='if_fyi'
    login_pwd='@Ye123456'
    wp=wp_plugin(login_url,login_user,login_pwd)

    md_urls='http://www.4xiaoshuo.com/29/29057/'
    urls=urls_collect(md_urls)
    # print(urls)
    if urls is not None:
        txt=parse_post(md_urls,urls)
        while True:
            p=next(txt)
            #print(p[0],p[1])
            wp.push_posts(p[0],p[1],['三寸人间'],None,None)
            #wp.check_post(1)
        print(time.strftime('%H:%M:%S'),':文章更新完成!!!')
    else:
        print(time.strftime('%H:%M:%S'),':文章最近没有更新!!!')
