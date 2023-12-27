from wb_tools import auto_notify, ping_test
from data.mtd.mastodon import Mastodon
from data.weibo.weibo import Weibo
import utils

def task():

    wb_switch = utils.read_config('config.ini')['WEIBO']['switch']
    mtd_switch = utils.read_config('config.ini')['MASTODON']['switch']

    task_list = []
    if wb_switch == 'y':
        task_list.append(Weibo())
    if mtd_switch == 'y':
        task_list.append(Mastodon())

    for t in task_list:
        # t.processor_work()
        try:
            t.processor_work()
        except:
            auto_notify.sys_notify('调用异常',t.__class__.__name__+'调用异常，请即时处理')

if __name__ == '__main__':
    # 网络环境检测
    ping_result = ping_test.network_ping()
    if not ping_result:
        print('network exception')
    else:
        expired = auto_notify.work()
        if not expired:
            task()
