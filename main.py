from wb_tools import auto_notify, ping_test
from data.mtd.mastodon import Mastodon
from data.weibo.weibo import Weibo
import utils

def task(task_list):
    for t in task_list:
        try:
            t.processor_work()
            print('=' * 20)
        except:
            auto_notify.sys_notify('调用异常',t.__class__.__name__+'调用异常，请即时处理')

def init():
    
    # 读取配置
    config = utils.read_config('config.ini')
    channel = config['CHANNEL']['list'].split(',')
    task_list = []
    for chn in channel:
        switch = config[chn]['switch']
        cron = config[chn]['cron']
        if switch == 'y' and (cron == 'default' or utils.is_time_scheduled(cron)):
            task_list.append(builder(chn))
    return task_list

def builder(chn):
    if chn == 'WEIBO':
        return Weibo()
    if chn == 'MASTODON':
        return Mastodon()

if __name__ == '__main__':
    # 网络环境检测。如果无网络环境，则直接退出。
    ping_result = ping_test.network_ping()
    if not ping_result:
        print('network exception')
    else:
        task_list = init()
        expired = auto_notify.work(task_list)
        if not expired:
            task(task_list)
        else:
            print('expired=' + str(expired))    
