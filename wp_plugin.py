import urllib,os,time,random,zhconv
from pyquery import PyQuery as pq
from wordpress_xmlrpc import Client,WordPressPost,WordPressTerm
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost,EditPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods import taxonomies,posts,media
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.compat import xmlrpc_client
class wp_plugin:
    def __init__(self,login_url,urser,pwd):
        self.url=login_url
        self.urser=urser
        self.pwd=pwd
        self.wp=self.login_func()        
    def login_func(self): 
        wp=Client(self.url,self.urser,self.pwd)
        return wp

    def check_post(self,num):
        posts=self.wp.call(GetPosts({'number':num}))
        for i in posts:
            print(i.id,'-',i.title,'-',i.post_status)

    def push_posts(self,title,content,categrory,tag,img_list):
        post = WordPressPost()
        post.title=title
        post.content=content
        post_categrory=categrory
        if tag is not None:
            post.terms_names={
                'post_tag':tag,
                'category':post_categrory
                }
        else:
            post.terms_names={
                'post_tag':[],
                'category':post_categrory
                }        
        post.post_status = 'publish'
        if img_list is not None:
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
        postid =self.wp.call(NewPost(post))
        print('正在发布[ID]:%s-[标题]:%s' %(postid,post.title))

    def edit_post(self,post_id,title,content,categrory,tag):
        post = WordPressPost()
        post.title=title
        post.content=content
        post_categrory=[]
        post_categrory.append(categrory)
        if tag is not None:
            post.terms_names={
                'post_tag':tag,
                'category':post_categrory
                }
        else:
            post.terms_names={
                'post_tag':[],
                'category':post_categrory
                }
        post.post_status = 'publish'
        self.wp.call(EditPost(post_id, post))
        print('正在修正[ID]:%s,[标题]:%s' %(post_id,post.title))

    def delet_post(self,post_id):
        post=WordPressPost()
        post.post_status='trash'
        self.wp.call(EditPost(post_id, post))
        print('正在删除[ID]:%s 的文章;' %(post_id,post.title))
