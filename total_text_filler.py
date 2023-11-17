from pyquery import PyQuery as pq
import requests
from urllib.parse import urlencode  # 导入urlencode函数，用于构建URL参数

def totalize_text(id, text):
    base_url = 'https://m.weibo.cn/'

    # <a href="/status/4884565010943284">全文</a>
    new_text = get_long_text(id)
    if new_text == '':
        new_text = text.replace('/status/', base_url + 'status/')
    return new_text


# 获取长微博
def get_long_text(id):
    headers_longtext = {
        'Host': 'm.weibo.cn',
        'Referer': 'https://m.weibo.cn/status/' + str(id),
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    }
    params = {
        'id': id
    }
    url = 'https://m.weibo.cn/statuses/extend?' + urlencode(params)

    response = requests.get(url, headers=headers_longtext)  # 发送HTTP GET请求
    if response.status_code == 200:  # 如果响应状态码为200（成功）
        jsondata = response.json()  # 解析JSON响应数据
        tmp = jsondata.get('data')  # 获取长文本数据
        return pq(tmp.get("longTextContent")).text() # 解析长文本内容
    else:
        return ''