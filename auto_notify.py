import requests
from datetime import datetime
import weibo
from mastodon import Mastodon

def work():
    notify_msg = ''
    try:
        wb = weibo.Weibo()
        text = wb.request_for_pages(0)
        if text.find('passport.weibo.cn') != -1:
            notify_msg = notify_msg + ('微博过期\n')
            notify_msg = notify_msg + text + '\n'
        mastodon = Mastodon()
        text = mastodon.request_for_pages(0)
        # 略
        if text.find(''):
            notify_msg = notify_msg + ('mastodon过期\n')
    except Exception:
        notify_msg = notify_msg + ('【weibo-proj】网络请异常')

    notify_msg = notify_msg + str(datetime.now()) + '\n'
    print(notify_msg)

    # send notify
    # Todo 这里自行填入你的通知接口地址
    notify_url = 'your-notify-url'
    params = {
        'title': '【weibo-proj】过期信息:',
        'content': notify_msg,
    }
    response = requests.get(notify_url, params=params)
    print(response.text)

if __name__ == '__main__':
    work()