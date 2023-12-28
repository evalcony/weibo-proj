import os
from datetime import datetime

import utils


class GroupByWeibo:
    def __init__(self):
        # result_dict['group_name'][winfo_list]
        self.result_dict = {}
        # user_group['group_name'][id_str_list]
        self.user_group = self.read_config()
        self.user_group_set = self.to_set()
        self.DIR = utils.read_config('config.ini')['DIR']

    def to_set(self):
        group_set = {}
        for n, l in self.user_group.items():
            group_set[n] = set(l)
        return group_set

    def read_config(self):
        # 创建 ConfigParser 对象
        config = utils.read_config('focus_user.ini')
        return self.get_section(config)

    def get_section(self, config):
        try:
            group = dict(config['USER_GROUP'].items())
            for k, v in group.items():
                if v == '':
                    group[k] = []
                else:
                    l = v.replace(' ', "").split(',')
                    group[k] = l
            return group
        except:
            return {}

    def work(self, page_list):
        # 根据 screen_name 进行分组
        for page in page_list:
            self.group(page)
        # save group
        self.save_group()

    def group(self, page):
        if self.user_group_set == {}:
            return
        gs = self.user_group_set
        for g_name, gs_id_set in gs.items():
            if len(gs_id_set) == 0:
                continue
            for winfo in page.winfo_list:
                id = winfo.user.id
                if str(id) in gs_id_set:
                    if g_name not in self.result_dict:
                        self.result_dict[g_name] = []
                    self.result_dict[g_name].append(winfo)

    def save_group(self):
        if self.result_dict == {}:
            return
        print('分组写文件开始')
        now = datetime.now()
        time_str = now.strftime('%Y-%m-%d')

        for name, w_list in self.result_dict.items():
            self._save_infront(time_str, name+'.html', w_list)
            print(f'分组写{name} 完成')

        print('分组写文件结束')

    def _save_infront(self, prefix, file_name, winfo_list):
        export_root_path = self.DIR['export_root_path']
        directory = export_root_path + '/weibo/group/' + prefix
        # 防止路径不存在
        if not os.path.exists(directory):
            os.makedirs(directory)

        # 若目录下不存在文件，则先创建，再写入内容
        dir_file_path = directory+'/' + file_name
        if not os.path.exists(dir_file_path):
            open(dir_file_path, 'w').close()
        with open(dir_file_path, 'r+') as f:
            original_content = f.read()
            f.seek(0)
            for w in winfo_list:
                str = w.as_weibo()
                f.write(str)
            f.write('\n')
            f.write(original_content)


def test_build_winfo(id, name):
    from data.weibo.winfo import Winfo
    from data.weibo.user import User
    winfo = Winfo('Sun Nov 26 13:00:01 +0800 2023', 1, '测试内容', User(id, name))
    return winfo


def test():
    winfo_list = []

    winfo = test_build_winfo(1, 'aaa')
    winfo_list.append(winfo)

    gbw = GroupByWeibo()
    gbw._save_infront('2023-03-31', 'group_article.html', winfo_list)

if __name__ == '__main__':
    test()