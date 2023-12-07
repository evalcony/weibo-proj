import sys

import requests
import os
from datetime import datetime

import utils
from data.weibo import weibo
from data.mtd.mastodon import Mastodon

config = utils.read_config('config.ini')
AUTO_NOTIFY = config['AUTO_NOTIFY']
MAC_SYS_NOTIFY = config['mac_sys_notify']

def work():

    # 自动通知开关
    notify_switch = AUTO_NOTIFY['notify_switch']
    if notify_switch != 'y':
        return

    notify_msg = ''
    expired = False
    try:
        wb = weibo.Weibo()
        text = wb.request_for_pages(0)
        if text.find('passport.weibo.cn') != -1:
            notify_msg = notify_msg + ('微博过期\n')
            notify_msg = notify_msg + text + '\n'
            expired = True
        mastodon = Mastodon()
        text = mastodon.request_for_pages(0)
        # 略
        if text.find(''):
            notify_msg = notify_msg + ('mastodon过期\n')
            expired = True
    except Exception:
        notify_msg = notify_msg + ('【weibo-proj】网络请求异常')

    notify_msg = notify_msg + str(datetime.now()) + '\n'
    print(notify_msg)

    params = {
        'title': '【weibo-proj】过期信息:',
        'content': notify_msg,
    }

    if MAC_SYS_NOTIFY == 'y':
        # macOS系统通知
        sys_notify(params)
    # send notify
    if expired:
        # 自动通知接口地址
        notify_url = AUTO_NOTIFY['url']
        response = requests.get(notify_url, params=params)
        print(response.text)
    else:
        print('接口正常，未过期')
    return expired

def sys_notify(params):
	os.system("""osascript -e 'display notification "{}" with title "{}"'""".format(params['content'], params['title']))

if __name__ == '__main__':
    work()
