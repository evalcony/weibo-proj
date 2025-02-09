import os
import time
import pickle
import argparse
from data.weibo.groupby_weibo import GroupByWeibo

CACHE_META_FILE = 'cache_meta.pkl'
CACHE_DATA_FILE = 'data_{id}.pkl'
root_dir = os.path.dirname(os.path.abspath(__file__))
CACHE_PATH = root_dir+'/cache/wb/{date}'

print(CACHE_PATH)

class CacheMeta:
    def __init__(self):
        self.begin_id = ''
        self.last_id = ''
        self.is_finished = False
        self.files = []

# todo
# 隔天处理的问题，需要注意

def done(target_day=''):

    # 删除相关数据
    cache_meta = read_cache_meta(target_day)
    remove_cache_files(cache_meta.files, target_day)

    # 重置cache_meta
    cache_meta = CacheMeta()
    cache_meta.is_finished = True
    write_cache_meta(cache_meta, target_day)

# 加载所有cache，并自动合并
def read_cache(target_day=''):

    # 加载meta数据
    cache_meta = read_cache_meta(target_day)

    # 根据cache_meta.files数组，加载所有dump文件数据
    total_page_list = []
    for file in cache_meta.files:
        # 合并各个dump文件
        tmp_page = load_dump(file, target_day)
        total_page_list.append(tmp_page)
    # 根据 sort_func 降序排序
    res_page_list = sorted(total_page_list, key=sort_func, reverse=True)

    # 返回page_list
    return res_page_list

def read_cache_meta(target_day=''):
    return load_dump(CACHE_META_FILE, target_day=target_day)

def is_empty(target_day=''):
    cache_meta = read_cache_meta(target_day)
    print(cache_meta.files)
    return len(cache_meta.files) == 0

def sort_func(page):
    return page.max_id

def write_cache(maxid, page, target_day=''):
    print('-' * 10 + '缓存数据开始')
    try:
        # 持久化page数据-----------
        cur_cache_data_file = _get_cache_data_filename(maxid)
        print(cur_cache_data_file)
        dump(page, cur_cache_data_file, target_day)

        # 持久化meta数据-----------
        cache_meta = load_dump(CACHE_META_FILE, target_day)
        cache_meta.is_finished = False
        # 更新last_id
        if cache_meta.last_id == '':
            print('设置last_id=' + maxid)
            cache_meta.last_id = maxid
        else:
            if cache_meta.last_id > maxid:
                print('更新last_id=' + maxid)
                cache_meta.last_id = maxid
        # 更新begin_id
        if cache_meta.begin_id == '':
            print('设置begin_id=' + maxid)
            cache_meta.begin_id = maxid
        else:
            if cache_meta.begin_id < maxid:
                print('更新begin_id=' + maxid)
                cache_meta.begin_id = maxid

        # 去重
        exist = False
        for file in cache_meta.files:
            if file == cur_cache_data_file:
                exist = True
                break
        if not exist:
            cache_meta.files.append(cur_cache_data_file)
        # 根据id从大到小排序
        cache_meta.files.sort(reverse=True)
        print(cache_meta.files)
        # 持久化
        write_cache_meta(cache_meta, target_day)
    except Exception as e:
        print(repr(e))
    print('-' * 10 + '缓存数据结束')

def write_cache_meta(cache_meta, target_day=''):
    dump(cache_meta, CACHE_META_FILE, target_day)

def _get_cachepath(path, target_day=''):
    if target_day == '':
        time.time()
        ymd = time.strftime("%Y-%m-%d")
        return path.replace('{date}', ymd)
    else:
        return path.replace('{date}', target_day)

def _get_cache_data_filename(maxid):
    return CACHE_DATA_FILE.replace('{id}', str(maxid))

# 数据序列化并持久化
def dump(data, filename, target_day=''):
    serialized_data = pickle.dumps(data)

    PATH = _get_cachepath(CACHE_PATH, target_day)
    if not os.path.exists(PATH):
        os.makedirs(PATH)
    # 打开文件
    with open(PATH+'/'+filename, "wb") as f:
        # 将序列化后的对象写入文件
        f.write(serialized_data)

def load_dump(filename, target_day=''):
    dir = _get_cachepath(CACHE_PATH, target_day)+'/'+filename
    if not os.path.exists(dir):
        print(dir)
        return CacheMeta()

    with open(dir, "rb") as f:
        # 读取原始文件
        serialized_data = f.read()
        # 反序列化对象
        deserialized_data = pickle.loads(serialized_data)
        return deserialized_data

def remove_cache_files(files, target_day=''):
    print('删除cache data文件 ' + target_day)
    path = _get_cachepath(CACHE_PATH, target_day)
    for file in files:
        if os.path.exists(path+'/'+file):
            os.remove(path+'/'+file)

# 读取指定日期的cache历史数据
# 语法 py wb_local_cache.py -d yyyy-MM-dd > ~/Desktop/temp.txt
# 语法 py wb_local_cache.py -d yyyy-MM-dd -f > ~/Desktop/temp.txt
# -f 命令会自动将数据写入当天export数据中。但是不会删除 cache 文件，需要手动删除。
def read_history_cache():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', type=str, default='', help='日期')
    parser.add_argument('-meta', type=str, default='', help='日期')
    parser.add_argument('-f', action='store_true', help='写入当天文件')
    args = parser.parse_args()

    if args.meta != '':
        target_day = args.meta
        cache_meta = read_cache_meta(target_day)
        print(cache_meta.begin_id)
        print(cache_meta.last_id)
        print(cache_meta.is_finished)
        # cache_meta.is_finished = True
        # write_cache_meta(cache_meta, target_day)

    if args.d != '':
        page_list = read_cache(args.d)
        for page in page_list:
            for winfo in page.winfo_list:
                print(winfo.as_weibo())

        if args.f:
            p = GroupByWeibo()
            p.work(page_list, args.d)

if __name__ == '__main__':
    read_history_cache()