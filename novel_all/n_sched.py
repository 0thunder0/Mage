import time,datetime,os,random
from apscheduler.schedulers.blocking import BlockingScheduler
def func():
    cmd='python novel_all.py'
    #  cmd_1='python novel_x23us.py'
    #  cmd_2='python novel_biquge.py'
    os.system(cmd)
    #  os.system(cmd_1)
    #  os.system(cmd_2)

def dojob():
    #创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    intc=random.randint(45,60)
    scheduler.add_job(func,'cron',hour=6, minute=intc)
    scheduler.add_job(func,'cron',hour=11, minute=intc)
    scheduler.add_job(func,'cron',hour=17, minute=intc)
    scheduler.add_job(func,'cron',hour=19, minute=intc)
    scheduler.add_job(func,'cron',hour=21, minute=intc)
    scheduler.start()
if __name__=='__main__':
    #dojob()
    func()
