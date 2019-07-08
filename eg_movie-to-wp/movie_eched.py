import time,datetime,os,random
from apscheduler.schedulers.blocking import BlockingScheduler

def func():
    cmd_1='python leadership-USshow.py'
    cmd_2='python leadership-dm.py'
    os.system(cmd_1)
    os.system(cmd_2)

def dojob():
    #创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    intc=random.randint(25,59)
    scheduler.add_job(func,'cron',hour=6, minute=intc)
    scheduler.add_job(func,'cron',hour=17, minute=intc)
    scheduler.start()

if __name__=='__main__':
    dojob()
