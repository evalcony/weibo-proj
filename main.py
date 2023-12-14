from tools import auto_notify, ping_test
from data.mtd.mastodon import Mastodon
from data.weibo.weibo import Weibo


def task():
    task_list = []
    task_list.append(Weibo())
    task_list.append(Mastodon())

    for t in task_list:
        try:
            t.processor_work()
        except:
            auto_notify.sys_notify('调用异常','调用异常，请即时处理')

if __name__ == '__main__':
    # 网络环境检测
    ping_result = ping_test.network_ping()
    if not ping_result:
        print('network exception')
    else:
        expired = auto_notify.work()
        if not expired:
            task()
