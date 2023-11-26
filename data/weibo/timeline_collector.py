import os
from datetime import datetime

import utils



class TimelineCollector:
    def __init__(self):
        print('weibo TimelineCollector')
        # self.read_from_config()
        self.DIR = utils.read_config('config.ini')['DIR']
        

    def test_work(self, page_list):
        print('timecollector test_work')

    def work(self, page_list):
        self.save_page_list(page_list)

    def save_page_list(self, page_list):
        print('写文件开始')
        now = datetime.now()
        time_str = now.strftime('%Y-%m-%d-%H-%M')
        print(time_str)

        export_root_path = self.DIR['export_root_path']
        with open(export_root_path + 'weibo/' + time_str + '.html', 'w') as f:
            for page in page_list:
                for winfo in page.winfo_list:
                    str = winfo.as_weibo()
                    f.write(str)
        print('写文件完成')


if __name__ == '__main__':
    tc = TimelineCollector()
    print(tc.timeline_url)