import time,datetime,os,random
from apscheduler.schedulers.blocking import BlockingScheduler
def func():
    cmd='python leadership.py'
    os.system(cmd)

def dojob():
    #创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    intc=random.randint(45,60)
    scheduler.add_job(func,'cron',hour=17, minute=intc)
    scheduler.start()

if __name__=='__main__':
    dojob()