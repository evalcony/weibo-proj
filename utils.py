import configparser
import random
import os
from datetime import datetime
import croniter

def read_config(name):
    # 创建 ConfigParser 对象
    config = configparser.RawConfigParser()
    # 读取配置文件
    config.read(file_path('config/'+name))
    return config

def write_config(config, name):
    # 将修改后的配置写回文件
    config_path = file_path('config/'+name)
    with open(config_path, 'w') as configfile:
        config.write(configfile)

def read_file(filename):
    lines = []
    root_dir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(root_dir+filename):
        return []
    with open(root_dir+filename, 'r') as file:
        for line in file:
            lines.append(line.replace("\n",""))
    return lines

def write_file(filename, lines, mode='w'):
    print('写入文件:', filename)
    root_dir = os.path.dirname(os.path.abspath(__file__))
    path = root_dir
    # 防止路径不存在
    if not os.path.exists(path):
        os.makedirs(path)
    dir_file_path = path + '/' + filename
    if not os.path.exists(dir_file_path):
        open(dir_file_path, 'w').close()
    with open(dir_file_path, 'w') as f:
        for m in lines:
            f.write(m+'\n')

def read_dirpath_file(filename):
    lines = []
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as file:
        for line in file:
            lines.append(line.replace("\n", ""))
    return lines

def write_dirpath_file(filename, lines):
    print('写入文件:', filename)
    with open(filename, 'w') as f:
        for m in lines:
            f.write(m + '\n')

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

# 判断当前时间是否满足定时任务执行表达式
def is_time_scheduled(cron_expression):
    # 获取当前时间
    now = datetime.datetime.now()
    # 创建cron迭代器
    ci = croniter.croniter(cron_expression, now)
    # 获取下一个执行时间
    next_time = ci.get_next(datetime.datetime)
    # 判断当前时间是否是执行时间
    return now == next_time


if __name__ == '__main__':

    d1 = 'Fri Mar 31 13:30:49 +0800 2023'
    print(format_time(d1))
