import urllib,os,time,random,zhconv
from pyquery import PyQuery as pq
from wordpress_xmlrpc import Client,WordPressPost,WordPressTerm
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost,EditPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods import taxonomies,posts,media
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.compat import xmlrpc_client

class tim_collect:
    def __init__(self,cache_log):
        UA=[
            "Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11"
        ]
        self.headers={"User-Agent":random.choice(UA)}
        if not os.path.isfile(cache_log):
            os.mknod(cache_log)
        with open(cache_log,'r+') as f:
            self.tim_cache=f.readlines()
        if len(self.tim_cache):
            for n in range(len(self.tim_cache)):
                self.tim_cache[n]=self.tim_cache[n].replace('\n','')
        self.imgs_list=[]
    def cat_url(self,first_url,cahce_log):
        req=urllib.request.Request(first_url,headers=self.headers)
        page_source= urllib.request.urlopen(req).read()
        page_source=page_source.decode('big5','ignore')
        data=pq(page_source)
        cat_urls=data('.forum-card .pic').items()
        for post_url in cat_urls:
            url='http://www.timliao.com/bbs/'+post_url('a').attr('href')
            if url not in self.tim_cache:
                with open(cache_log,'a+') as f:
                    f.writelines(url+'\n')
                yield url

    def detail_parse(self,url):
        req = urllib.request.Request(url, headers=self.headers)
        data = urllib.request.urlopen(req).read()
        data=data.decode('big5','ignore')
        page_data=pq(data)
        content_title=page_data('.table_fixed tr td h1').text()
        post_title=self.zhconv_convert(content_title)
        #print(post_title)
        content_content=page_data('.mt10').text()
        content_text=self.zhconv_convert(content_content)+'\n'
        #print(content_text)
        img_items=page_data('.mt10 a').items()
        content_imgs=''
        imgs_list=[]
        #创建图片文件存储位置
        for img_item in img_items:
            img_url=img_item('img').attr('src')
            if img_url:
                #urllib.request.urlretrieve(img_url,img_path)
                content_text=content_text+'<img src="'+img_url+'" class="item img-fluid">'+'\n'
                self.imgs_list.append(img_url)
        #print(post_title,content_text+'\n'+content_imgs,imgs_list)
        return post_title,content_text,self.imgs_list
    
    #下载图片到otl.ooo这域名下
    def parse_img(self,post_id,img_list):
        new_img_list=[]
        for img_url in img_list:
            img_local_path='/www/wwwroot/otl.ooo/Imghub_'+str(post_id)
            img_local_absolutePath=img_local_path+'/'+img_url.split('?')[0].split('/')[-1]
            img_local_absolutePath=img_local_absolutePath.replace(' ','')
            print('图片保存地址：',img_url,img_local_path,img_local_absolutePath)
            if not os.path.isdir(img_local_path):
                os.makedirs(img_local_path)
            urllib.request.urlretrieve(img_url,img_local_absolutePath)
            new_img_list.append(img_local_absolutePath.replace('/www/wwwroot/','http://'))
        return new_img_list
    
    #转简体
    def zhconv_convert(self,content):
        shield_word=['多图／','【短篇报导】','【新春特辑】','【长篇报导】','【正妹贴图】','▲文章来源:','提姆正妹','&#13;','▲文章报导：（图／翻摄自脸书&IG）','正妹部落客']
        typec=type(content)
        if typec==str:        
            txt=zhconv.convert(content,'zh-cn')        
            for wd in shield_word:
                txt=txt.replace(wd,'')
            return txt
        else:
            print(typec)
class wp_push_post:
    def __init__(self,login_url,urser,pwd):
        self.url=login_url
        self.urser=urser
        self.pwd=pwd
        self.wp=self.login_func()        
    def login_func(self): 
        wp=Client(self.url,self.urser,self.pwd)
        return wp

    def push_posts(self,title,content,categrory,tag,img_list):
        post = WordPressPost()
        post.title=title
        post.content=content
        post.categrory=[]
        post.categrory.append(categrory)
        
        if tag:
            post.tag=[]
            post.tag.append(tag)
            post.terms_names={
                'post_tag':post.tag,
                'category':post.categrory
            }
        else:
            post.terms_names={
                'post_tag':'',
                'category':post.categrory
            }
        post.post_status = 'publish'
        if img_list:
            for i in range(len(img_list)):
                img_name=img_list[i].split('/')[-1]
                filename = './'+img_name
                #上传的图片本地文件路径 
                # prepare metadata
                data = {'name': 'picture.jpg','type': 'image/jpeg',}
                data['name']=img_name
            # read the binary file and let the XMLRPC library encode it into base64
                with open(filename, 'rb') as img:
                    data['bits'] = xmlrpc_client.Binary(img.read())
                response=self.wp.call(media.UploadFile(data))
                if i ==len(img_list)-1:
                    attachment_id = response['id']
                    post.thumbnail=attachment_id
            '''
            response == {
              'id': 6,
              'file': 'picture.jpg'
              'url': 'http://www.example.com/wp-content/uploads/2012/04/16/picture.jpg',
              'type': 'image/jpeg',
            }
            '''
        postid = self.wp.call(NewPost(post))        
        print('正在发布[ID]:%s,[标题]:%s' %(postid,post.title))
        return postid,len(post.content)
            
    def edit_post(self,post_id,title,content,categrory,post_tag,img_list):
        post = WordPressPost()
        post.title=title
        post.content=content
        post.categrory=[]
        post.categrory.append(categrory)
        if post_tag is not None:
            post.terms_names={
                'post_tag':post_tag,
                'category':post.categrory
            }
        else:
            post.terms_names={
                'post_tag':'',
                'category':post.categrory
            }
        post.post_status = 'publish'
        self.wp.call(EditPost(post_id, post))
        print('正在修正[ID]:%s,[标题]:%s' %(post_id,post.title))
        return post_id,len(post.content)

if __name__=='__main__':
    
    login_url='http://if.fyi/xmlrpc.php'
    login_root='if_fyi'
    login_pwd='@Ye123456'
    wp=wp_push_post(login_url,login_root,login_pwd)
    
    cache_log='url-cache.log' #去重用的url缓存文件
    tim_cat=tim_collect(cache_log)
    #采集tim目录
    urls=tim_cat.cat_url('http://www.timliao.com/bbs/forumdisplay_beauty_wall.php?fid=18&filter=5000000&orderby=dateline&page=1',cache_log)
    #解析目录中文章网址,处理采集到的内容
    post_id_cache='post_id_cache.log'
    if not os.path.isfile(post_id_cache):
        os.mknod(post_id_cache)
    with open(post_id_cache,'r') as f:
        list_1=f.readlines()
    while True:
        p_url=next(urls)
        print('cat_url 函数执行完成',p_url)
        post=tim_cat.detail_parse(p_url)        
        title=post[0]
        content=post[1]
        categrory='others'
        tag=''
        feature_list=[]
        img_list=[]
        #记录文章id和网址
        if len(list_1) <= 200 : 
            #发布文章到wp
            posts=wp.push_posts(title,content,categrory,tag,feature_list)
            print(posts[0],post[2])
            img_list=tim_cat.parse_img(posts[0],post[2])
            print('输出parse_img函数 返回值：',img_list)
            
            for img in img_list:
                img_label='<img src="'+img+'" class="item img-fluid">'+'\n'
                content=content+img_label
            feature_list.append(img_list[-1])
            wp.edit_post(posts[0],title,content,categrory,tag,feature_list)
            with open(post_id_cache,'a+') as f:
                f.writelines(posts[0]+'|'+p_url+'\n')
            break
        else:
            #发布文章到wp
            post_id=list_1[0].split('|')[0]
            for index in range(len(list_1)-1):
                list_1[i]=list_1[i+1]
            wp.edit_post(post_id,title,content,categrory,tag,img_list)
            list_1[-1]=post_id+'|'+p_url+'\n'
            with open(post_id_cache,'w+') as f:
                f.writelines(list_1)
            break
    #保存img网址为log文件，并下载
