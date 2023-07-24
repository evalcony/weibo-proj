import auto_notify
from mastodon import Mastodon
from weibo import Weibo
import ping_test


def task():
    task_list = []
    task_list.append(Weibo())
    task_list.append(Mastodon())

    for t in task_list:
        t.processor_work()

if __name__ == '__main__':
    # 网络环境检测
    ping_result = ping_test.network_ping()
    if not ping_result:
        print('network exception')
    else:
        expired = auto_notify.work()
        if not expired:
            task()
