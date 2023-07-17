import argparse
import requests

import utils
from mastodon import Mastodon
from weibo import Weibo


def get_proxy():
    config = utils.read_config('config.ini')
    # 代理服务器
    return {
        "http": config['PROXY']['http_proxy'], 
        "https": config['PROXY']['https_proxy'],
    }

def request_for_google():
    # 禁用 SSL 验证
    requests.packages.urllib3.disable_warnings()
    response = requests.get("https://www.google.com", verify=False, timeout=5, cert=None, proxies=get_proxy())
    return response.content

def request_for_v2ex():
    response = requests.get("https://www.v2ex.com", verify = False, timeout=5, cert=None, proxies=get_proxy())
    return response.content

def request_for_baidu():
    response = requests.get("https://www.baidu.com", verify = False, )
    return response.content

def ping(args):
    text = ''
    if args.w:
        wb = Weibo()
        text = wb.request_for_pages(0)
    if args.m:
        mastodon = Mastodon()
        text = mastodon.request_for_pages(0)
    if args.v:
        text = request_for_v2ex()
    if args.g:
        text = request_for_google()
    if args.b:
        text = request_for_baidu()

    print(text[:100])
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # path
    parser.add_argument('-m', action='store_true', help='ping 长毛象')
    parser.add_argument('-w', action='store_true', help='ping weibo')
    parser.add_argument('-v', action='store_true', help='ping v2ex')
    parser.add_argument('-g', action='store_true', help='ping google')
    parser.add_argument('-b', action='store_true', help='ping baidu')
    args = parser.parse_args()
    ping(args=args)
