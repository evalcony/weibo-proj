from wb_tools import auto_notify, ping_test
from data.mtd.mastodon import Mastodon
from data.weibo.weibo import Weibo
import utils

def task():
    # 读取配置
    config = utils.read_config('config.ini')
    wb_switch = config['WEIBO']['switch']
    mtd_switch = config['MASTODON']['switch']
    mastodon_cron = config['MASTODON']['cron']

    task_list = []
    if wb_switch == 'y':
        task_list.append(Weibo())
    if mtd_switch == 'y' and (mastodon_cron == 'default' or utils.is_time_scheduled(mastodon_cron)):
        task_list.append(Mastodon())

    for t in task_list:
        try:
            t.processor_work()
            print('=' * 20)
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
