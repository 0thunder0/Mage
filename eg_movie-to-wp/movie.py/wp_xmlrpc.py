import urllib,os,time,random,zhconv,shutil
from wordpress_xmlrpc import Client,WordPressPost,WordPressTerm
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost,EditPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods import taxonomies,posts,media
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.compat import xmlrpc_client

class wp_push:
    def __init__(self,*args):
        self.url=args[0]
        self.user=args[1]
        self.pwd=args[2]
        
        if len(args)>3:
            self.wp_log=args[3]
            if not os.path.isfile(self.wp_log):
                os.mknod(self.wp_log)
        
        self.wp=self.login_func()

    def login_func(self): 
        wp=Client(self.url,self.user,self.pwd)
        return wp

    def push_posts(self,title,feature_img,staff,content,img_list,tag_list,categrory):
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
        #如果特色图片存在，那么加到图片列表最后一张
        if feature_img:
            img_list.append(feature_img)
        #上传图片到wp
        if img_list:
            for i in range(len(img_list)):
                img_name=img_list[i].split('/')[-1]
                filename =img_list[i]
                #上传的图片本地文件路径 
                # prepare metadata
                data = {
                        'name': img_name,
                        'type': 'image/jpeg'
                        }
                #data['name']=img_name
            # read the binary file and let the XMLRPC library encode it into base64
                with open(filename, 'rb') as img:
                    data['bits'] = xmlrpc_client.Binary(img.read())
                response=self.wp.call(media.UploadFile(data))
                #取最后一张图片作为特色图片
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
        #  if os.path.isfile(self.wp_log):
            #  with open(self.wp_log,'a+') as f:
                #  f.writelines(str(postid)+'\n')
        return postid

    def edit_posts(self,post_id,title,feature_img,staff,content,img_list,tag_list,categrory):
        post = WordPressPost()
        post.title=title
        if staff:
            content=staff+'<br>'+content
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
        #img_list设置为空，避免图片重复上传
        img_list=[]
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
        if os.path.isfile(self.wp_log):
            with open(self.wp_log,'a+') as f:
                f.writelines(str(post_id)+'\n')
        return post_id,len(post.content)

    #下载图片到otl.ooo这域名下
    def parse_img(self,post_id,img_list,local_abspath):
        if type(post_id) is not str:
            post_id=str(post_id)
        if not os.path.isdir(local_abspath):
            os.makedirs(local_abspath)
        new_img_list=[]
        for img_url in img_list:
            img_url=img_url.split('!')[0]
            print('开始下载图片:%s' %img_url)
            img_local_path=local_abspath+post_id
            img_local_absolutePath=img_local_path+'/'+img_url.split('?')[0].split('/')[-1]
            #print('图片保存地址：',img_url,img_local_path,img_local_absolutePath)
            if not os.path.isdir(img_local_path):
                os.makedirs(img_local_path)
            try:
                urllib.request.urlretrieve(img_url,img_local_absolutePath)
            except:
                print('图片下载失败:',img_url)
            #new_img_list.append(img_local_absolutePath.replace('/www/wwwroot/','http://'))
            new_img_list.append(img_local_absolutePath)
        return new_img_list

    #删除制定目录
    def trash_img(self,post_id):
        path='/www/wwwroot/otl.ooo/IMAGE/'+str(post_id)
        shutil.rmtree(path)

if __name__=='__main__':
    loginUrl='http://if.fyi/xmlrpc.php'
    loginUser='if_fyi'
    loginPw='HZGWYpCtrPWZJ7kA'
    wpLog='wo_log.log'
    wp=wp_push(loginUrl,loginUser,loginPw,wpLog)
    title='11111111'
    content='2222222222'
    img_list=[]
    tag_list=[]
    category='333'
    wp.push_posts(title,content,img_list,tag_list,category)
