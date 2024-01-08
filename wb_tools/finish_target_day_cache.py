import argparse
import datetime
import sys

sys.path.append('..')
from data.weibo.weibo import Weibo
import wb_local_cache
from wb_tools import auto_notify

# 补全指定日期的缓存数据

def main(args):
    if args.j:
        print('执行每日cache_clean job')
        daily_cache_clean()
        return

    if args.d != '':
        print(args.d)
        do_cache(args.d)
        return

# 每日job，检查前一天缓存数据是否全部落地。如果没有，则主动执行
def daily_cache_clean():
    yesterday_str = get_yesterday()
    print(yesterday_str)
    empty = wb_local_cache.is_empty(yesterday_str)
    print(str(empty))
    if empty:
        # delete file
        return
    else:
        # 发送消息通知
        auto_notify.sys_notify('缓存数据遗留', yesterday_str+'缓存数据遗留')
        # 处理缓存数据
        result = do_cache(yesterday_str)
        auto_notify.sys_notify('缓存数据遗留-处理结果', yesterday_str + '处理结果：'+str(result))

        return

def get_yesterday():
    # 获取当前日期
    now = datetime.datetime.today()

    # 获取前一天的日期
    yesterday = now - datetime.timedelta(days=1)

    # 格式化日期
    yesterday_str = yesterday.strftime('%Y-%m-%d')

    return yesterday_str

# 手动清理缓存
def do_cache(target_day):
    wb = Weibo()
    result = wb.solve_cache(target_day=target_day)
    print(str(result))

# 使用方法
# py finish_target_day_cache.py -d 2024-01-01
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', type=str, default='', help='日期')
    parser.add_argument('-j', action='store_true', help='job')
    args = parser.parse_args()
    main(args)