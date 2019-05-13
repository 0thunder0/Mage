import urllib,os,time,random,zhconv
from pyquery import PyQuery as pq
from wordpress_xmlrpc import Client,WordPressPost,WordPressTerm
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost,EditPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods import taxonomies
# from wp_plugin import wp_plugin
headers = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
#从文章目录中采集文章网址
def collect_page_list(num):
    url_lists=[]
    detail_urls=[]
    for num in range(1,num):
        url_lists.append('http://www.timliao.com/bbs/forumdisplay_beauty_wall.php?fid=18&filter=5000000&orderby=dateline&page=%s' %num)
    for url in url_lists:
        req = urllib.request.Request(url, headers=headers)
        data = urllib.request.urlopen(req).read()
        data=data.decode('big5','ignore')
        page_source=pq(data)
        urls=page_source('.forum-card .pic').items()
        for url in urls:
            try:
                detail_urls.append('http://www.timliao.com/bbs/'+url('a').attr('href'))
            except:
                continue
        #print(detail_urls)
        page_url_parse(detail_urls)
#文章内容采集处理
def page_url_parse(urls_cache):
    urls=urls_cache
    for url in urls[::-1]:
        req = urllib.request.Request(url, headers=headers)
        data = urllib.request.urlopen(req).read()
        data=data.decode('big5','ignore')
        page_data=pq(data)
        content_title=page_data('.table_fixed tr td h1').text()
        post_title=zhconv_convert(content_title)
        #print(post_title)
        content_content=page_data('.mt10').text()
        content_text=zhconv_convert(content_content)
        #print(content_text)
        img_items=page_data('.mt10 a').items()
        content_imgs=''
        imgs_list=[]
        #创建图片文件存储位置           
        for img_item in img_items:
            img_url=img_item('img').attr('src')
            if img_url is not None:
                img_path='./'+img_url.split('/')[-1]
                urllib.request.urlretrieve(img_url,img_path)
                content_imgs=content_imgs+'<img src="'+img_url+'" class="item">'
                imgs_list.append(img_path)
        #print(content_imgs)
        #发布文章
        push_post_to_wordpress(post_title,content_text+'\n'+content_imgs,imgs_list)
def push_post_to_wordpress(title,text,img_list):
    wp=Client('http://if.fyi/xmlrpc.php','if_fyi','@Ye123456')
    post=WordPressPost()
    print(title)
    #发布文章到wordpress
    post.title=title
    post.content=text
    post_category=['others']
    post.post_status = 'publish'  
    #文章状态，不写默认是草稿，private表示私密的，draft表示草稿，publish表示发布
    post.terms_names={
    'post_tag':['test','firstpost'],
    'category':post_category
    }
    #发布图片
    img_list=[]
    if img_list is not None:
        for i in range(len(img_list)):
            img_name=img_list[i].split('/')[-1]
            #上传的图片本地文件路径 
            # prepare metadata
            data = {'name': 'picture.jpg','type': 'image/jpeg',}
            data['name']=img_name
            # read the binary file and let the XMLRPC library encode it into base64
            with open(img_list[i], 'rb') as img:
                data['bits'] = xmlrpc_client.Binary(img.read())
            response=wp.call(media.UploadFile(data))
            if i ==len(img_list)-1:
                attachment_id = response['id']
                post.thumbnail=attachment_id
    time.sleep(random.randint(5,10))
    post_id=wp.call(NewPost(post))
    print('正在发布[ID]:%s,[标题]:%s' %(post_id,post.title))
#转简体
def zhconv_convert(content):
    shield_word=['多图／','【短篇报导】','【新春特辑】','【长篇报导】','【正妹贴图】','▲文章来源:','提姆正妹','&#13;','▲文章报导：（图／翻摄自脸书&IG）']
    typec=type(content)
    if typec==str:        
        txt=zhconv.convert(content,'zh-cn')        
        for wd in shield_word:
            txt=txt.replace(wd,'')
        return txt
    else:
        print(typec)
if __name__=='__main__':
    #页码输入从3开始
    collect_page_list(2)
