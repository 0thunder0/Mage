import os,time,re
from wp_xmlrpc import wp_push
from Eurl_yyetss import mv_plugin

class leaderShip:
    def __init__(self,loginUrl,loginUser,loginPw,wpLog):
        #默认登录wp
        self.loginUrl=loginUrl
        self.loginUser=loginUser
        self.loginPw=loginPw
        self.wpLog=wpLog
        #提取缓存文件，leaderShip.log
        self.cacheD=[]
        if os.path.isfile(self.wpLog):
            with open(self.wpLog,'r+') as f:
                self.cacheD=f.readlines()
        self.wp=wp_push(self.loginUrl,self.loginUser,self.loginPw,self.wpLog)

    def sp_posts(self):
        #采集前的初始化
        mv=mv_plugin()
        plotUrls=mv.categoryParse()
        while True:
            plots=next(plotUrls)
            plot=mv.contentParse(plots)
            self.wpSched(plot)

    def wpSched(self,plot):
        url=plot[0]
        title=plot[1]
        feature_img=plot[2]
        img_list=plot[3]
        staff=plot[4]
        content=plot[5]
        download_area=plot[6]
        try:
            post_cache=url+'_'+str(len(content+download_area))
            x=0
            if self.cacheD:
                for n in range(len(self.cacheD)):
                    if re.search(url,self.cacheD[n]):
                        if re.search(post_cache,self.cacheD[n]):
                            print('内容完全没有更新 ！！！')
                            x=x+1
                            break
                        else:
                            self.editToWp(plot)
                            x=x+1
                            break
                if x<1:
                    self.pushToWp(plot)
            else:
                self.pushToWp(plot)
        except:
            print('没有采集到下载资源……')

    def editToWp(self,*plot):
        plot=plot[0]
        url=plot[0]
        title=plot[1]
        feature_img=plot[2]
        img_list=plot[3]
        staff=plot[4]
        content=plot[5]
        download_area=plot[6]
        #寻找已发布文章id
        post_id=0
        for n in range(len(self.cacheD)):
            if re.search(url,self.cacheD[n]):
                post_ids=self.cacheD[n].split('_')[-1].replace('\n','')
                post_id=int(post_ids)
                print('已发布文章id',post_id,type(post_id))
                #用最新的文章情况替换掉老的
                self.cacheD[n]=url+'_'+str(len(content+download_area))+'_'+str(post_id)+'\n'
            else:
                self.cacheD[n]=self.cacheD[n]+'\n'
        #避免重复上传 feature_img,img_list
        feature_img=''
        img_list=[]
        tag_list=[]
        category='美剧'
        self.wp.edit_posts(post_id,title,feature_img,staff,content,img_list,tag_list,category)
        #将新的缓存存入缓存文件
        #print('缓存url文件:',self.cacheD)
        with open(self.wpLog,'w+') as f:
            f.writelines(self.cacheD)

    def pushToWp(self,*plot):
        plot=plot[0]
        url=plot[0]
        title=plot[1]
        feature_img=plot[2]
        img_list=plot[3]
        staff=plot[4]
        content=plot[5]
        download_area=plot[6]
        tag_list=[]
        category='美剧'
        post_content=content+'<br>'+download_area
        #图片本地化
        if feature_img:
            if type(feature_img)==list:
                img_list=img_list+feature_img
            else:
                img_list.append(feature_img)
                feature_img=''

        nowTime=time.strftime('%Y%m%d',time.localtime(time.time()))
        local_abspath='/www/wwwroot/otl.ooo/movie_img/'
        img_list=self.wp.parse_img(nowTime,img_list,local_abspath)
        #push_posts(self,title,feature_img,staff,content,img_list,tag_list,category)
        post_id=self.wp.push_posts(title,feature_img,staff,post_content,img_list,tag_list,category)
        cache_temp=url+'_'+str(len(content+download_area))+'_'+str(post_id)+'\n'
        self.cacheD.append(cache_temp)
        #print('缓存url文件:',self.cacheD)
        with open(self.wpLog,'w+') as f:
            f.writelines(self.cacheD)

if __name__=='__main__':
    loginUrl='http://7oh.net/xmlrpc.php'
    loginUser='edjo@7oh.net'
    loginPw='43PvHfxsfqCIl*5MFk'
    wpLog='7oh_net.log'
    leader=leaderShip(loginUrl,loginUser,loginPw,wpLog)
    #leader.push_func()
    leader.sp_posts()
