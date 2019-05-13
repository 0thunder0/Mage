import urllib,os,time,random,zhconv,shutil
from pyquery import PyQuery as pq
from wordpress_xmlrpc import Client,WordPressPost,WordPressTerm
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost,EditPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods import taxonomies,posts,media
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.compat import xmlrpc_client

class wp_push_post:
    def __init__(self,login_url,urser,pwd,wp_log):
        self.url=login_url
        self.urser=urser
        self.pwd=pwd
        self.wp_log=wp_log
        if not os.path.isfile(self.wp_log):
            os.mknod(self.wp_log)
        self.wp=self.login_func()

    def login_func(self): 
        wp=Client(self.url,self.urser,self.pwd)
        return wp

    def push_posts(self,title,content,img_list,tag_list,categrory):
        post = WordPressPost()
        post.title=title
        post.content=content
        post.categrory=[]
        post.categrory.append(categrory)
        if tag_list:
            post.terms_names={
                'post_tag':tag_list,
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
        with open(self.wp_log,'a+') as f:
            f.writelines(str(postid)+'\n')
        return postid,len(post.content)

    def edit_post(self,post_id,title,content,img_list,tag_list,categrory):
        post = WordPressPost()
        post.title=title
        post.content=content
        post.categrory=[]
        post.categrory.append(categrory)
        if tag_list:
            post.terms_names={
                'post_tag':tag_list,
                'category':post.categrory
            }
        else:
            post.terms_names={
                'post_tag':'',
                'category':post.categrory
            }
        if img_list:
            img_name=img_list[-1].split('/')[-1]
            filename=img_list[-1].replace('http://','/www/wwwroot/')
            data={'name':img_name,'type':'image/jpeg'}
            try:
                with open(filename,'rb') as img:
                    data['bits']=xmlrpc_client.Binary(img.read())
                response=self.wp.call(media.UploadFile(data))
                attachment_id = response['id']
                post.thumbnail=attachment_id
            except:
                print('最后一张图片不存在:',img_list[-1])
        #    for i in range(len(img_list)):
        #        img_name=img_list[i].split('/')[-1]
        #        filename = './'+img_name
                #上传的图片本地文件路径 
                # prepare metadata
        #        data = {'name': 'picture.jpg','type': 'image/jpeg',}
        #        data['name']=img_name
            # read the binary file and let the XMLRPC library encode it into base64
        #        with open(filename,'rb') as img:
        #            data['bits'] = xmlrpc_client.Binary(img.read())
        #        response=self.wp.call(media.UploadFile(data))
        #        if i ==len(img_list)-1:
        #            attachment_id = response['id']
        #            post.thumbnail=attachment_id
        post.post_status = 'publish'
        self.wp.call(EditPost(post_id, post))
        print('正在修正[ID]:%s,[标题]:%s' %(post_id,post.title))
        with open(self.wp_log,'a+') as f:
            f.writelines(str(post_id)+'\n')
        return post_id,len(post.content)
    #下载图片到otl.ooo这域名下
    def parse_img(self,post_id,img_list):
        new_img_list=[]
        for img_url in img_list:
            img_local_path='/www/wwwroot/otl.ooo/IMAGE/'+str(post_id)
            img_local_absolutePath=img_local_path+'/'+img_url.split('?')[0].split('/')[-1]
            #print('图片保存地址：',img_url,img_local_path,img_local_absolutePath)
            if not os.path.isdir(img_local_path):
                os.makedirs(img_local_path)
            try:
                urllib.request.urlretrieve(img_url,img_local_absolutePath)
            except:
                print('图片下载失败:',img_url)
            new_img_list.append(img_local_absolutePath.replace('/www/wwwroot/','http://'))
        return new_img_list
    #删除制定目录
    def trash_img(self,post_id):
        path='/www/wwwroot/otl.ooo/IMAGE/'+str(post_id)
        shutil.rmtree(path)
