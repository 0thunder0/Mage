from wp_plugin import wp_plugin 
import time,random,os,urllib
from pyquery import PyQuery as pq
urls=['http://www.hizbo.com/meinv/']
#header={"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"}
header={'User-Agent':'Opera/9.80(Macintosh;IntelMacOSX10.6.8;U;en)Presto/2.8.131Version/11.11'}

def urls_collect(cat_url,cache_txt):
    req=urllib.request.Request(cat_url,headers=header)
    data = urllib.request.urlopen(req).read()
    page_source=pq(data)
    #提取小说名字
    cat=page_source('.info h2').text()
    #读取链接存档文件,用来判断是否重复
    if not os.path.isfile(cache_txt):
        os.mknod(cache_txt)
    with open(cache_txt,'r+') as f:
        novelCache=f.readlines()
    for i in range(len(novelCache)):
        novelCache[i]=novelCache[i].replace('\n','')
    #采集所有文章链接
    novel_list=[]
    urls=page_source('.listmain dd').items()    
    for ur in urls:
        url_cache=ur('a').attr('href')
        url_cache=cat_url+url_cache
        if url_cache not in novelCache:
            novel_list.append(url_cache)
    lists=list(set(novel_list))
    lists.sort()
    #给文章链接排序
    return lists,cat

def parse_post(cache_txt,post_urls):
    with open(cache_txt,'a+') as f:
        for r_url in post_urls:
            f.writelines(r_url+'\n')
            #print(r_url)
            req=urllib.request.Request(r_url,headers=header)
            data = urllib.request.urlopen(req).read()
            data=pq(data)
            title=data('.content h1').text()
            content=data('#content').text()
            yield title,content
#屏蔽关键词
def shield_word(content):
    with open('shield_word.txt','r+') as f:
        words=f.readlines()
        for w in words:
            w=w.replace('\n','')
            content=content.replace(w,'')
    return content

if __name__=='__main__':

    login_url='http://if.fyi/xmlrpc.php'
    login_user='if_fyi'
    login_pwd='HZGWYpCtrPWZJ7kA'
    wp=wp_plugin(login_url,login_user,login_pwd)

    url_all=[
    'http://www.4xiaoshuo.com/37/37505/',
    'http://www.4xiaoshuo.com/29/29057/',
    'http://www.4xiaoshuo.com/52/52737/',
    'http://www.4xiaoshuo.com/22/22479/'
    ]
    cache_txt='cache_url.txt'
    for num in range(len(url_all)):
        post_list=urls_collect(url_all[num],cache_txt)
        urls=post_list[0]
        cat=[]
        cat.append(post_list[1])
        #print(urls)
        if len(urls) == 0:
            print(time.strftime('%H:%M:%S'),':文章最近没有更新!!!')
        else:
            txt=parse_post(cache_txt,urls)
            try:
                while True:
                    p=next(txt)
                    title=shield_word(p[0])
                    content=shield_word(p[1])
                #print(title,content,cat)
                    wp.push_posts(title,content,cat,None,None)
            except:
                print(time.strftime('%H:%M:%S'),':更新完成!!!')
