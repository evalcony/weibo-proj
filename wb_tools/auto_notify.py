import sys
import requests
import os
from datetime import datetime
import utils

# 读取配置
config = utils.read_config('config.ini')
AUTO_NOTIFY = config['AUTO_NOTIFY']


def work(task_list):
    # 自动通知开关
    NOTIFY_SWITCH = AUTO_NOTIFY['notify_switch']
    if NOTIFY_SWITCH != 'y':
        return

    # 过期检测
    notify_msg = ''
    expired = False
    try:
        print('len(task_list) = ' + str(len(task_list)))
        for agent in task_list:
            agt_exp = agent.is_expire()
            print(f'{agent.name()}.is_expire:{agt_exp}')
            if agt_exp:
                notify_msg = notify_msg + agent.name()+"过期\n"
                expired = True
    except Exception as e:
        print(e)
        notify_msg = notify_msg + ('【weibo-proj】网络请求异常')

    # 如果过期了，发送系统通知消息
    if expired:
        notify_msg = notify_msg + str(datetime.now()) + '\n'
        send_notify(notify_msg)
    return expired

def send_notify(notify_msg):
    params = {
        'title': '【weibo-proj】过期信息:',
        'content': notify_msg,
    }

    # macOS系统通知
    sys_notify('【weibo-proj】过期信息', '微博过期')

    # 自动通知接口地址
    NOTIFY_URL = AUTO_NOTIFY['url']
    response = requests.get(NOTIFY_URL, params=params)
    print(response.text)

def sys_notify(title, content):
    MAC_SYS_NOTIFY = AUTO_NOTIFY['mac_sys_notify']
    if MAC_SYS_NOTIFY == 'y':
        os.system("""osascript -e 'display notification "{}" with title "{}"'""".format(content, title))

if __name__ == '__main__':
    work()
