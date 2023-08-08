import argparse
import utils

# 处理 forbidden_words.txt，可以追加、删除

base_file = 'forbidden_words.txt'

def add(word):
    file_path = utils.file_path(base_file)
    with open(file_path, 'a') as f:
        f.write(word + '\n')
    print('写入成功：' + word)

def delete(word):
    fbw_list = read_file('raw-list')
    file_path = utils.file_path(base_file)
    with open(file_path, 'w') as f:
        for w in fbw_list:
            if w != word + '\n':
                f.write(w)

    print('删除成功：' + word)

def find(word):
    words = read_file('set')
    if word in words:
        return True
    else:
        return False

def compare(sentence):
    flg = False
    words = read_file('set')
    for word in words:
        if sentence.find(word) != -1:
            flg = True
            print('命中:', word)
            break
    if not flg:
        print('未命中')


def read_file(type):
    if type == 'set':
        words = set()
        file_path = utils.file_path(base_file)
        with open(file_path, 'r') as file:
            for line in file:
                pl = len(words)
                s = set(line.split())
                words |= s
                nl = len(words)
                if pl == nl:
                    print('出现重复:' + line)
        return words
    elif type == 'raw-list':
        words = []
        file_path = utils.file_path(base_file)
        with open(file_path, 'r') as file:
            for line in file:
                words.append(line)
        return words

def manager(args):
    if args.a:
        if not find(args.a):
            add(args.a)
        else:
            print('已存在：' + args.a)
    elif args.d:
        if find(args.d):
            delete(args.d)
        else:
            print('未找到: '+ args.d)
    elif args.f:
        if find(args.f):
            print('重复')
        else:
            print('未发现')
    elif args.l:
        s = read_file('set')
        print(s)
    elif args.c:
        compare(args.c)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', type=str, default='', help='增加words')
    parser.add_argument('-d', type=str, default='', help='删除words')
    parser.add_argument('-f', type=str, default='', help='搜索words')
    parser.add_argument('-c', type=str, default='', help='判断输入内容是否命中屏蔽词')
    parser.add_argument('-l', action='store_true', help='列出所有 forbidden words')
    args = parser.parse_args()

    manager(args)
