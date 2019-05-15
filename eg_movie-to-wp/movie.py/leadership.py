import os
from wp_xmlrpc import wp_push
from Eurl_yyetss import mv_plugin

class leaderShip:
    def __init__(self,loginUrl,loginUser,loginPw,wpLog):
        #默认登录wp
        self.loginUrl=loginUrl
        self.loginUser=loginUser
        self.loginPw=loginPw
        self.wpLog=wpLog
        #采集前的初始化
        self.mv=mv_plugin()
        url='http://www.yyetss.com'
        self.urls=self.mv.categroryParse(url)
        #提取缓存文件，leaderShip.log
        self.cacheD=[]
        if not os.path.isfile('leaderShip.log'):
            os.mknod('leaderShip.log')
        else:
            with open('leaderShip.log','r+') as f:
                self.cacheD=f.readlines()
            for n in range(len(self.cacheD)):
                self.cacheD[n]=self.cacheD[n].replace('\n','')

    def push_func(self):
        wp=wp_push(self.loginUrl,self.loginUser,self.loginPw,self.wpLog)
        while True:
            plots=next(self.urls)
            plot=self.mv.contentParse(plots)
            # return url,title,feature_img,imgs,staff,plot,downloadArea
            url=plot[0]
            title=plot[1]
            feature_img=plot[2]
            img_list=plot[3]
            staff=plot[4]
            content=plot[5]
            download_area=plot[6]
            tag_list=[]
            category=''
            content=content+'<br>'+download_area
            #push_posts(self,title,feature_img,staff,content,img_list,tag_list,category)
            wp.push_posts(title,feature_img,staff,content,img_list,tag_list,category)
            break

if __name__=='__main__':
    loginUrl='http://if.fyi/xmlrpc.php'
    loginUser='if_fyi'
    loginPw='HZGWYpCtrPWZJ7kA'
    wpLog='wo_log.log'
    leader=leaderShip(loginUrl,loginUser,loginPw,wpLog)
    leader.push_func()
