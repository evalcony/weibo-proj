import argparse

import utils


def update(section, option, value):
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
    if args.u:
        update(args.section, args.option, args.value)
    elif args.show:
        show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-section', type=str, default='', help='命名空间')
    parser.add_argument('-option', type=str, default='', help='key')
    parser.add_argument('-value', type=str, default='', help='value')
    parser.add_argument('-u', action='store_true', help='update config')
    parser.add_argument('-show', action='store_true', help='print config')
    args = parser.parse_args()

    work(args)