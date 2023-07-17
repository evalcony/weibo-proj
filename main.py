import auto_notify
from mastodon import Mastodon
from weibo import Weibo


def task():
    task_list = []
    task_list.append(Weibo())
    task_list.append(Mastodon())

    for t in task_list:
        t.processor_work()

if __name__ == '__main__':
    auto_notify.work()
    task()
