import argparse
import os
import sys

# 获取当前脚本所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 将项目的根目录添加到 Python 模块搜索路径中
proj_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(proj_root)
import utils


def update(update_param):
    # 解析参数
    key_end_pos = update_param.find('=')
    arg_left = update_param[:key_end_pos]
    arg_right = update_param[key_end_pos+1:]
    key_arr = arg_left.split('.')

    section = key_arr[0]
    option = key_arr[1]
    value = arg_right

    config = utils.read_config('config.ini')
    config.set(section, option, value)

    # 对 cookie 的情况特殊处理
    if section == 'WEIBO' and option == 'cookie':
        values = value.split(';')
        for v in values:
            if v.find('mweibo_short_token') != -1:
                token_arr = v.split('=')
                config.set(section, 'token', token_arr[1].strip())

    utils.write_config(config, 'config.ini')

def show():
    config = utils.read_config('config.ini')
    for section in config.sections():
        print(f"[Section: {section}]")
        for option, value in config.items(section):
            print(f"{option} = {value}")
        print('')

def work(args):
    if args.u != '':
        update(args.u)
    elif args.show:
        show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', type=str, default='', help='update config的参数。遵循section.option.value 的写法')
    parser.add_argument('-show', action='store_true', help='print config')
    args = parser.parse_args()

    work(args)