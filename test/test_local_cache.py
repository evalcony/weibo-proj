import os
import sys
import time

# 获取当前脚本所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 将项目的根目录添加到 Python 模块搜索路径中
proj_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(proj_root)

import wb_local_cache
from data.weibo.page import Page
from data.weibo.winfo import Winfo
from data.weibo.user import User

def test_write():
    # 生成测试数据
    page_list = []
    winfo_list = []
    for i in range(5):
        winfo = Winfo('Tue Dec 26 11:00:00 +0800 2023', str(i*i), 'text_'+str(i), User(str(i), 'screen_name_'+str(i)))
        # print(winfo.as_weibo())
        winfo_list.append(winfo)
    page = Page(winfo_list, 0, 100, time.time())
    page_list.append(page)

    # 序列化
    wb_local_cache.write_cache('1', page_list)

def test_read():
    page_list = wb_local_cache.read_cache()
    sum = 0
    print('page_list.size=' + str(len(page_list)))
    print()

    for page in page_list:
        winfo_list = page.winfo_list
        print(page.max_id)
        sum += len(winfo_list)
        # for winfo in winfo_list:
        #     print(winfo.as_weibo())
    print('总条数 = ' + str(sum))

def test_sort():
    page_list = []
    page_list.append(Page([], 1, 1, '111'))
    page_list.append(Page([], 1, 1, '222'))
    res = sorted(page_list, key=wb_local_cache.sort_func, reverse=True)
    for page in res:
        print(page.max_id)

def generate_maxid_list():
    id_list = []
    for i in range(5):
        id_list.append(str(id))
    return id_list

def test_reset_cache_meta():
    # 谨慎使用
    cache_meta = wb_local_cache.CacheMeta()
    cache_meta.files = ['data_0.pkl', 'data_4983574910472099.pkl', 'data_4983571284493290.pkl', 'data_4983567748956197.pkl',
     'data_4983564537956536.pkl', 'data_4983560295159278.pkl', 'data_4983556298245107.pkl', 'data_4983550317955233.pkl',
     'data_4983545997037035.pkl', 'data_4983542333574799.pkl', 'data_4983539925783040.pkl', 'data_4983536989766011.pkl',
     'data_4983534039860933.pkl']
    cache_meta.begin_id = '0'
    cache_meta.last_id = '4983534039860933'

    print(cache_meta.begin_id)
    print(cache_meta.last_id)
    print(cache_meta.is_finished)
    print(cache_meta.files)

    # 更新meta数据
    wb_local_cache.write_cache_meta(cache_meta)

def test_cache_meta():
    cm = wb_local_cache.read_cache_meta()
    print(cm.begin_id)
    print(cm.last_id)
    print(cm.is_finished)
    print(cm.files)

def test_cache_data():
    test_write()
    print('-' * 20)
    test_read()
    test_sort()

def test_done():
    print('wb_local_cache.done')
    wb_local_cache.done()

    print('read cache_meta')
    cm = wb_local_cache.read_cache_meta()
    print(cm.is_finished)
    print(cm.files)

def test_sort():
    list = ['data_4983641724421799.pkl', 'data_4983628923408930.pkl', 'data_4983632387903350.pkl', 'data_4983636996134374.pkl']
    list.sort(reverse=True)
    print(list)



if __name__ == '__main__':

    # test_reset_cache_meta() # 重置meta数据
    test_cache_meta() # 读meta数据
    # test_cache_meta()
    # test_sort()
    # test_done()