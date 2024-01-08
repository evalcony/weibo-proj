
import requests
import wb_local_cache
import utils
import time
import json
from data.filter import Filter
from data.weibo.groupby_weibo import GroupByWeibo
from data.weibo.page import Page
from data.weibo.retweeted_status import RetweetedStatus
from data.weibo.timeline_collector import TimelineCollector
from data.weibo.user import User
from data.weibo.winfo import Winfo


class Weibo:
    def __init__(self):
        print('weibo..')
        # 读取配置
        self.read_from_config()
        self.filter = Filter()

        # 注册处理器
        self.processor_list = []
        self._regist_processor()

    # 读取上一次更新的位置
    def read_from_config(self):
        config = utils.read_config('config.ini')

        self.last_id = config['WEIBO']['last_id']
        self.created_at = config['WEIBO']['created_at']
        self.cookie = config['WEIBO']['cookie']
        self.token = config['WEIBO']['token']
        self.timeline_url = config['WEIBO']['timeline_url']
        self.processors = config['WEIBO']['processors'].replace(' ', "").split(',')

        print('config------------------------------------------------------')
        print(self.last_id)
        print(self.created_at)
        print('config------------------------------------------------------')

    def get_processors(self):
        return self.processors
    def _regist_processor(self):
        print('注册 weibo processors')
        for p in self.processors:
            print('注册: ' + p)
            self.processor_list.append(self._build_weibo_processor(p))

    def _build_weibo_processor(self, type):
        if (type == 'timeline'):
            return TimelineCollector()
        if (type == 'group'):
            return GroupByWeibo()
        else:
            return TimelineCollector()
    
    def get_page_list(self, max_id=0):
        page_list = []
        end_point = False
        while True:
            try:
                text = self.request_for_pages(max_id)
            except Exception as e:
                print(repr(e))
                return [], False

            # 解析得到分页数据，一个page中包含 statuses，即多条winfo
            page = self.parse_json(text)

            if page == None:
                print('未从http请求中得到page数据')
                break
            if len(page.winfo_list) == 0:
                break
            # 这里更新id，是为了处理 max_id=0的情况
            max_id = page.winfo_list[0].id

            # 将每个page数据缓存
            wb_local_cache.write_cache(max_id, page)

            page_list.append(page)
            max_id = page.max_id

            # 判断是否到达结束点
            continuable = self.is_continue(page)
            if not continuable:
                # 只有为True时，是明确的抵达结束点
                end_point = True
                print('不需继续执行，退出')
                break

            sleep_time = utils.random_num(1, 30)
            print(f'wait {sleep_time}s......')
            time.sleep(sleep_time)

        print(f'page_list={len(page_list)} end_point={end_point}')
        return page_list, end_point

    # 基于 created_at 来判断是否要继续拉取数据
    def is_continue(self, page):
        if len(page.winfo_list) == 0:
            return True
        config_created_at = self.created_at

        last_raw_created_at = page.get_raw_last_created_at()
        d1 = utils.format_time(config_created_at)
        d2 = utils.format_time(last_raw_created_at)
        is_smaller = utils.is_smaller_than(d1, d2)
        print(f'{d1} < {d2} = {is_smaller}')
        return is_smaller

    # 发送 HTTP 请求
    def request_for_pages(self, max_id):

        param = f"max_id={max_id}"

        url = self.timeline_url
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'x-xsrf-token': self.token,
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip',
            'cookie': self.cookie,
        }
        if max_id != 0:
            url = self.timeline_url + param
        print(url)
        response = requests.get(url, headers=headers)
        try:
            if response.status_code == 200:
                return response.text
        except requests.ConnectionError as e:
            print('Error', e.args)

    def parse_json(self, json_text):
        print('parse_json...', json_text[:100])
        json_obj = json.loads(json_text)

        ok = json_obj['ok']
        print(f'ok={ok}')
        if ok != 1:
            return None
        data_obj = json_obj['data']
        previous_cursor = data_obj['previous_cursor']
        next_cursor = data_obj['next_cursor']
        max_id = data_obj['max_id']

        print(f'max_id={max_id}')

        winfo_list = []
        statuses = data_obj['statuses']
        for stat in statuses:
            try:
                winfo = self.build_winfo(stat)
            except Exception as e:
                print(repr(e))
                continue

            # 总是允许
            passable = self.filter.always_pass(winfo.user)
            if passable:
                winfo_list.append(winfo)
                continue

            # 过滤
            w1 = self.filter.has_forbidden_word(winfo.text)
            if w1 != '':
                print(f'触发过滤策略: {w1}')
                continue
            w2 = ''
            if winfo.has_retweeted:
                w2 = self.filter.has_forbidden_word(winfo.retweeted_status.text)
            if w2 != '':
                print(f'触发过滤策略: {w2}')
                continue
            winfo_list.append(winfo)
        print(f"len={len(winfo_list)}")
        print("*" * 20)

        page = Page(winfo_list, previous_cursor, next_cursor, max_id)
        return page

    def build_winfo(self, stat):
        created_at = stat['created_at']
        id = stat['id']
        text = stat['text']
        is_long_text = stat['isLongText']
        u = stat['user']
        user = User(u['id'], u['screen_name'])
        retweeted_status = None
        # 转发
        if 'retweeted_status' in stat:
            rs_json = stat['retweeted_status']
            retweeted_status = RetweetedStatus(rs_json)
        winfo = Winfo(created_at, id, text, user, retweeted_status, is_long_text)
        print(f'winfo:{winfo.created_at} {winfo.id} {winfo.user.id} {winfo.user.screen_name}')
        # print(winfo.__str__())
        return winfo

    def processor_work(self):

        # 每次开始，先处理历史未完成的 cache 数据
        flg = self.solve_cache()
        # 未成功抵达结束点，所以直接退出，不执行下面流程
        if not flg:
            print('缓存流程结束时，未成功抵达上一批次结束点')
            return

        # cache数据已经写文件后，再处理最新数据
        self.solve_latest()


    def solve_cache(self, target_day=''):
        cache_meta = wb_local_cache.read_cache_meta(target_day)
        if cache_meta.is_finished:
            return True
        # 如果未完成，则优先将cache直到上一次结束点的数据全部获取
        tuple = self.get_page_list(cache_meta.last_id)
        end_point = tuple[1]
        # 如果未读到结束点
        if not end_point:
            return False

        print('--------------solve_cache() 结束点 --------------')

        # 读取全量cache_page_list数据。因为上面的page_list是[截断点 -> 结束点]直接的数据
        cache_page_list = wb_local_cache.read_cache(target_day)

        if len(cache_page_list) == 0:
            print('cache_page_list=[]，结束')
            return False

        # 数据处理+更新 config, cache_meta
        self.process_data_and_update_config(cache_page_list, target_day)

        # 重新读取配置，更新内存中的相关配置
        self.read_from_config()

        return True

    def solve_latest(self):
        # 获取当前最新数据
        tuple = self.get_page_list()
        page_list = tuple[0]
        if len(page_list) == 0 or not tuple[1]:
            print(f'page_list={len(page_list)} end_point={tuple[1]}，结束')
            return False

        # 数据处理+更新 config, cache_meta
        self.process_data_and_update_config(page_list)

    def process_data_and_update_config(self, page_list, target_day=''):
        # 数据处理
        for p in self.processor_list:
            try:
                p.work(page_list, target_day)
            except Exception as e:
                print(repr(e))
                return

        # 更新 config
        last_id = page_list[0].winfo_list[0].id
        last_created_at = page_list[0].winfo_list[0].created_at
        self.update_config(last_id, last_created_at)

        # 更新cache_meta数据，重置cache_meta
        wb_local_cache.done(target_day)

        print('本次批次全部执行完毕')

    # 每次结束后，更新配置文件
    def update_config(self, id, created_at):
        config = utils.read_config('config.ini')

        # 更新
        config['WEIBO']['last_id'] = id
        config['WEIBO']['created_at'] = created_at

        # 将修改后的配置写回文件
        config_path = utils.file_path('config/config.ini')
        with open(config_path, 'w') as f:
            config.write(f)

        print('更新config.ini完成')

if __name__ == '__main__':
    print('hello')
    wb = Weibo()
    wb.processor_work()