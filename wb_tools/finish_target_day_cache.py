import argparse
import sys

sys.path.append('..')
from data.weibo.weibo import Weibo

# 补全指定日期的缓存数据

def main(args):
    if args.d == '':
        return
    print(args.d)

    wb = Weibo()
    result = wb.solve_cache(target_day=args.d)
    print(str(result))


# 使用方法
# py finish_target_day_cache.py -d 2024-01-01
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', type=str, default='', help='日期')
    args = parser.parse_args()
    main(args)