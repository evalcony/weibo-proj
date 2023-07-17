import requests
from datetime import datetime
import weibo
from mastodon import Mastodon

def work():
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
        notify_msg = notify_msg + ('【weibo-proj】网络请异常')

    notify_msg = notify_msg + str(datetime.now()) + '\n'
    print(notify_msg)

    # send notify
    if expired:
        # Todo 这里自行填入你的通知接口地址
        notify_url = 'https://push.showdoc.com.cn/server/api/push/5f9501a1d2504471d7314b96933019c91134058281'
        params = {
            'title': '【weibo-proj】过期信息:',
            'content': notify_msg,
        }
        response = requests.get(notify_url, params=params)
        print(response.text)
    else:
        print('接口正常，未过期')

if __name__ == '__main__':
    work()