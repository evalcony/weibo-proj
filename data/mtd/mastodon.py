import json
import os
import shutil
import time
from datetime import datetime
import requests
import utils
from data.mtd.mtd_Info import MtdInfo


class Mastodon:
    def __init__(self):
        self.read_from_config()
        self.result_dict = {}
        self.user_group_set = {}
        self.user_group_set = self.to_set()

    # 读取上一次更新的位置
    def read_from_config(self):
        config = utils.read_config('config.ini')

        self.DIR = config['DIR']
        self.created_at = config['MASTODON']['created_at']
        self.cookie = config['MASTODON']['cookie']
        self.timeline_url = config['MASTODON']['timeline_url']
        self.auth_key = config['MASTODON']['auth_key']
        self.proxy_switch = config['MASTODON']['proxy_switch']
        self.cron = config['MASTODON']['cron']
        # 代理服务器
        self.proxy = {
            "http": config['PROXY']['http_proxy'], 
            "https": config['PROXY']['https_proxy'],
        }

        print('mastodon config------------------------------------------------------')
        print("上次更新时间：" + self.created_at)
        print("接口请求地址：" + self.timeline_url)
        print("auth_key：" + self.auth_key)
        print("是否使用代理：" + self.proxy_switch)
        print("代理服务器地址：" + self.proxy["https"])
        print("定时任务频次：" + self.cron)
        print('mastodon config------------------------------------------------------')

    def to_set(self):
        # group_set = {}
        # for n, l in self.user_group.items():
        #     group_set[n] = set(l)
        # return group_set
        group_set = {}
        # Todo: 我的mastodon比较特殊，所以很个人的代码，这里就删掉了
        # 请使用者根据个人情况，自行编写相关代码
        return group_set

    # 每次结束后，更新配置文件
    def update_config(self, id, created_at):
        config = utils.read_config('config.ini')

        # 更新
        config['MASTODON']['last_id'] = id
        config['MASTODON']['created_at'] = created_at

        # 将修改后的配置写回文件
        config_path = utils.file_path('config/config.ini')
        with open(config_path, 'w') as f:
            config.write(f)

        print('更新config.ini完成')

    def is_expire(self):
        text = self.request_for_pages(0)
        return not (len(text) > 0)

    def name(self):
        return "mastodon"

    def request_for_pages(self, max_id):
        url = 'https://cr8r.gg/api/v1/timelines/home'
        if max_id != 0:
            url = url + '?max_id=' + str(max_id)
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': self.cookie,
            'Authorization': 'Bearer ' + self.auth_key,
            'X-Requested-With': 'XMLHttpRequest',
        }
        # 注意这里要用字符串
        response = requests.get(url, headers=headers, proxies= self.proxy if self.proxy_switch == "y" else None)
        try:
            if response.status_code == 200:
                return response.text
        except requests.ConnectionError as e:
            print('Error', e.args)

    def group(self, page):
        if self.user_group_set == {}:
            return
        mtd_list = page

        gs = self.user_group_set
        for g_name, gs_id_set in gs.items():
            if len(gs_id_set) == 0:
                continue

            for mtd in mtd_list:
                id = mtd.account.id
                if str(id) in gs_id_set:
                    if g_name not in self.result_dict:
                        self.result_dict[g_name] = []
                    self.result_dict[g_name].append(mtd)

    def save_group(self):
        if self.result_dict == {}:
            return
        print('mastodon分组写文件开始')
        now = datetime.now()
        time_str = now.strftime('%Y-%m')

        for name, m_list in self.result_dict.items():
            self._save_infront(time_str, name + '.html', m_list)
            print(f'分组写:{name} 完成')

        print('mastodon分组写文件结束')

    def _save_infront(self, prefix, file_name, mtd_list):
        export_root_path = self.DIR['export_root_path']
        directory = export_root_path + '/mastodon/group/' + prefix
        img_export_path = directory + '/medias'

        # 防止路径不存在
        if not os.path.exists(directory):
            os.makedirs(directory)

        # 若目录下不存在文件，则先创建，再写入内容
        dir_file_path = directory + '/' + file_name
        if not os.path.exists(dir_file_path):
            open(dir_file_path, 'w').close()
        with open(dir_file_path, 'r+') as f:
            original_content = f.read()
            f.seek(0)
            for m in mtd_list:
                self._save_medias(m, img_export_path)
                str = m.as_mastodon()
                f.write(str)
            f.write(original_content)

    # 保存多媒体资源（仅限图片）
    def _save_medias(self, mtd, img_export_path):
        media_attachments = mtd.media_attachments
        if media_attachments == []:
            return

        # 检查保存路径是否存在
        if not os.path.exists(img_export_path):
            os.makedirs(img_export_path)

        # 下载资源文件
        for url in media_attachments:
            response = requests.get(url, stream=True)
            filename = url.split('/')[-1]
            path = img_export_path+'/'+filename
            with open(path, "wb") as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            print('保存成功 ' + path)

    # 基于 created_at 来判断是否要继续拉取数据
    def is_continue(self, mtd):
        config_created_at = self.created_at

        last_raw_created_at = mtd.created_at
        d1 = utils.format_time2(config_created_at)
        d2 = utils.format_time2(last_raw_created_at)
        is_smaller = utils.is_smaller_than(d1, d2)
        print(f'{d1} < {d2} = {is_smaller}')
        return is_smaller

    def get_page_list(self):
        page_list = []
        max_id = 0
        while True:
            text = self.request_for_pages(max_id)

            # 解析得到分页数据
            page, continuable = self.parse(text)

            if page == None:
                print('未从http请求中得到page数据')
                break
            if len(page) == 0:
                break

            page_list.append(page)
            if not continuable:
                break
            max_id = page[-1].id

            sleep_time = utils.random_num(1, 10)
            print(f'wait {sleep_time}s......')
            time.sleep(sleep_time)

        return page_list

    def parse(self, json_data):
        page = []
        parsed_data = json.loads(json_data)
        for item in parsed_data:
            mtd = MtdInfo(item)

            continuable = self.is_continue(mtd)
            if not continuable:
                break
            page.append(mtd)
            print(mtd.content)

        print(f"len={len(page)}")
        print("*" * 20)
        return page, continuable

    def processor_work(self):

        page_list = self.get_page_list()
        if len(page_list) == 0:
            return
        for page in page_list:
            if len(page) == 0:
                continue
            self.group(page)
        self.save_group()

        last_id = page_list[0][0].id
        last_created_at = page_list[0][0].created_at
        self.update_config(last_id, last_created_at)

def test_build_mtd_info():
    item = dict()
    item["created_at"] = '2023-11-26T05:02:31.000Z'
    item["id"] = '1'
    item["url"] = 'url'
    item["content"] = 'content'

    account = dict()
    account['id'] = 'a_id'
    account['username'] = 'a_uname'
    account['display_name'] = 'a_disp_name'
    item['account'] = account

    item['reblog'] = None

    return MtdInfo(item)

def test():
    mtd_list = []
    mtd_list.append(test_build_mtd_info())

    mastodon = Mastodon()
    mastodon._save_infront('2023-04', '老周.html', mtd_list)

if __name__ == '__main__':
    # mastodon = Mastodon()
    # mastodon.processor_work()
    test()