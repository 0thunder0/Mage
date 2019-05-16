import os,time
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
            for n in range(len(self.cacheD)):
                self.cacheD[n]=self.cacheD[n].replace('\n','')
        self.wp=wp_push(self.loginUrl,self.loginUser,self.loginPw,self.wpLog)

    def sp_posts(self):
        #采集前的初始化
        mv=mv_plugin()
        plotUrls=mv.categoryParse()
        while True:
            plots=next(plotUrls)
            plot=mv.contentParse(plots)
            self.pushToWp(plot)

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
        category='333'
        content=content+'<br>'+download_area
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
        self.wp.push_posts(title,feature_img,staff,content,img_list,tag_list,category)

if __name__=='__main__':
    loginUrl='http://if.fyi/xmlrpc.php'
    loginUser='if_fyi'
    loginPw='HZGWYpCtrPWZJ7kA'
    wpLog='wo_log.log'
    leader=leaderShip(loginUrl,loginUser,loginPw,wpLog)
    #leader.push_func()
    leader.sp_posts()
