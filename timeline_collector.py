import os
from datetime import datetime

class TimelineCollector:
    def __init__(self):
        print('weibo TimelineCollector')
        # self.read_from_config()
        

    def test_work(self, page_list):
        print('timecollector test_work')

    def work(self, page_list):

        # save page_list
        self.save_page_list(page_list)

        # last_id = page_list[0].winfo_list[0].id
        # last_created_at = page_list[0].winfo_list[0].created_at
        # self.update_config(last_id, last_created_at)

    def save_page_list(self, page_list):
        print('写文件开始')
        now = datetime.now()
        time_str = now.strftime('%Y-%m-%d-%H-%M')
        print(time_str)

        root_dir = os.path.dirname(os.path.abspath(__file__))
        with open(root_dir+'/export/weibo/' + time_str + '.html', 'w') as f:
            for page in page_list:
                for winfo in page.winfo_list:
                    str = winfo.as_weibo()
                    f.write(str)
        print('写文件完成')


if __name__ == '__main__':
    tc = TimelineCollector()
    print(tc.timeline_url)