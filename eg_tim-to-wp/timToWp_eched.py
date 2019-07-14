import time,datetime,os,random
from timToWp_parse import tim_collect
from timToWp_push import wp_push_post
from apscheduler.schedulers.blocking import BlockingScheduler
def fun_c():
    tim_log='tim_url.log'
    tim_url='http://www.timliao.com/bbs/forumdisplay_beauty_wall.php?fid=18&filter=5000000&orderby=dateline'

    login_url='http://iyo.cx/xmlrpc.php'
    login_root='iyo_cx'
    login_pwd='$iyo.cx_jax.ye'
    wp_log='iyo_cx.log'
    wp=wp_push_post(login_url,login_root,login_pwd,wp_log)
    #采集模块
    tim=tim_collect(tim_log)
    try:
        urls=tim.cat_url(tim_url,tim_log)
    except:
        print('没有最新内容...')
    while True:
        try:
            url=next(urls)
        except:
            print('最近没有更新！！！')
            break
        if os.path.isfile(wp_log):
            with open(wp_log,'r+') as f:
                wp_post_list=f.readlines()
        else:
            wp_post_list=[]
        post=tim.detail_parse(url)
        #content_title,content_text,self.imgs_list,content_tag,content_categrory
        title=post[0]
        text=post[1].replace(' ','').replace('\n','')
        img_list=post[2]
        tag=post[3]
        cat='小姐姐'
        #print(post)
        #顺序不变去重,这里因为要先发布再修改,wp_log中一个id存了两行
        wp_list=wp_post_list
        wp_post_list=list(set(wp_post_list))
        wp_post_list.sort(key=wp_list.index)
        #wp_post_list.sort()
#        print(wp_post_list)
        if len(wp_post_list) > 300:
            print('文章数已经超过300篇....')
            post_id=wp_post_list[0].replace('\n','')
            wp.trash_img(int(post_id))
            img_list=wp.parse_img(post_id,img_list)
            print(len(img_list),'-文章中图片数量')
            text=text+'<div class="wpImgFluid">'
            for img in img_list:
                text=text+'<img src="'+img+'" class="img-fluid">'
            text=text+'</div>'
            wp.edit_post(post_id,title,text,img_list,tag,cat)
            for n in range(len(wp_post_list)-1):
                wp_post_list[n]=wp_post_list[n+1]
            wp_post_list.append(str(post_id)+'\n')
            with open(wp_log,'w+') as f:
                f.writelines(wp_post_list)
        else:
            print('更新最新文章...')
            post=wp.push_posts(title,text,[],tag,cat)
            post_id=post[0]
            img_list=wp.parse_img(post_id,img_list)
            text=text+'<div class="wpImgFluid">'
            for img in img_list:
                text=text+'<img src="'+img+'" class="img-fluid">'
            text=text+'</div>'
            #print(text)
            wp.edit_post(post_id,title,text,img_list,tag,cat)
            with open(wp_log,'a+') as f:
                f.writelines(str(post_id)+'\n')
def dojob():
    #创建调度器：BlockingScheduler
    sched = BlockingScheduler()
    intc=random.randint(30,59)
    sched.add_job(fun_c,'cron',hour=22, minute=intc)
    sched.start()
if __name__=='__main__':
    dojob()
    #fun_c()
