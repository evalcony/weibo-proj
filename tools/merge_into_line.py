import argparse
import os
import sys

sys.path.append("..")
import utils


# DEFAULT_WEIBO_EXPORT_PATH = utils.read_config('config.ini')['DIR']['export_root_path'] # 文件的路径前缀
DEFAULT_WEIBO_EXPORT_PATH = utils.read_config('config.ini')['DIR']['export_root_path_test'] # 测试路径-文件的路径前缀

def core(args):
    if args.d:
        # 自动填充路径
        dir = args.d
        if dir.find('../') != -1:
            file_below = dir[dir.find('../') + 3:]
            dir = os.path.dirname(os.path.abspath(__file__)) + DEFAULT_WEIBO_EXPORT_PATH + file_below
        traverse_directory(dir)
    elif args.a:
        dir = os.path.dirname(os.path.abspath(__file__)) + DEFAULT_WEIBO_EXPORT_PATH
        traverse_directory(dir)

def traverse_directory(directory):
    if os.path.isfile(directory):
        processor(directory)
    else:
        for root, dirs, files in os.walk(directory):
            # 遍历当前目录下的文件
            for file in files:
                file_path = os.path.join(root, file)
                if (file.find('.html') != -1):
                    processor(file_path)


def processor(filename):
    lines = utils.read_dirpath_file(filename)

    r_lines = []
    j = -2
    for i in range(len(lines)):
        if i <= j+1:
            continue
        if lines[i] == '':
            r_lines.append(lines[i])
            continue
        if lines[i].endswith('</p>') and lines[i+1] != '</br>':
            r_lines.append(lines[i])
            continue
        if lines[i].endswith('</p></br>'):
            r_lines.append(lines[i])
            continue
        else:
            j = next_br(lines, i)
            tmp = []
            for k in range(i+1, j):
                tmp.append(lines[k])
            res = '<br />'.join(tmp)

            r_lines.append(lines[i]+res+lines[j])

    utils.write_dirpath_file(filename, r_lines)

def next_br(lines, i):
    j = i
    while not lines[j].endswith('</br>'):
        j = j + 1
    return j

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', type=str, default='',
                        help='指定绝对路径的下的数据。也可以简化路径写法，以 ../ 开头，如 -d ../2023-07-16 其中，../ 表示省略路径之前的部分')
    parser.add_argument('-a', action='store_true', help='对全部文件进行处理')
    # parser.add_argument('-t', action='store_true', help='执行test')
    args = parser.parse_args()

    core(args)
