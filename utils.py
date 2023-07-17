import configparser
import random
import os
from datetime import datetime

def read_config(name):
    # 创建 ConfigParser 对象
    config = configparser.RawConfigParser()
    # 读取配置文件
    config.read(file_path(name))
    return config

def file_path(name):
    # 获取当前文件所在的根路径
    root_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(root_dir, name)
    return file_path

# 适用于 weibo 的日期数据
def format_time(time_str):
    date_obj = datetime.strptime(time_str, '%a %b %d %H:%M:%S %z %Y')
    formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')

    return formatted_date

# 适用于 mastodon 的日期数据
def format_time2(time_str):
    date_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date

def is_smaller_than(date1, date2):
    return date1 < date2

def random_num(l, r):
    return random.randint(l, r)

if __name__ == '__main__':

    d1 = 'Fri Mar 31 13:30:49 +0800 2023'
    print(format_time(d1))
