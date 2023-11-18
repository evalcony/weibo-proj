import os
import argparse
import utils
from datetime import datetime
from filter import Filter
from weibo_seperator import WeiboSeperator

class DataCleaner:
    def __init__(self):
        # read config user
        config = utils.read_config('focus_user.ini')
        self.user_set = self.get_user_set(config)

        # read config forbidden words
        self.filter = Filter()

    def get_user_set(self, config):
        try:
            group = dict(config['USER_GROUP'].items())
            for k, v in group.items():

                if v == '':
                    group[k] = []
                else:
                    l = v.replace(' ', "").split(',')
                    group[k] = l
            user_set = set()
            for k, v in group.items():
                user_set |= set(v)
            return user_set
        except Exception as e:
            print("exception: ", str(e))
            return ()

    def traverse_directory(self, directory):
        if os.path.isfile(directory):
            self.process(directory)
        else:
            for root, dirs, files in os.walk(directory):
                # 遍历当前目录下的文件
                for file in files:
                    file_path = os.path.join(root, file)
                    if (file.find('.html') != -1):
                        self.process(file_path)

    def process(self, file_path):
        file_root, file = os.path.split(file_path)
        # read data
        result = self.read_single_source(file_path)
        # clean data
        cr = self.clean_data(result)
        # write data
        self.save_result(cr, file_root, file)

    def read_single_source(self, file_path):
        result = []  # 存储结果的数组
        # root_dir = os.path.dirname(os.path.abspath(__file__))
        with open(file_path, 'r') as file:
            block = []  # 存储每个块的临时列表
            for line in file:
                line = line.strip()  # 去除行首行尾的空白字符

                if line:  # 如果行不为空
                    block.append(line)  # 将行添加到当前块
                elif block:  # 如果行为空且当前块不为空
                    result.append(''.join(block))  # 将当前块拼接成一个字符串并添加到结果数组
                    block = []  # 重置当前块

            if block:  # 处理文件结尾的块
                result.append(''.join(block))
        return result

    def clean_data(self, data):
        filt_res = []
        for d in data:
            tu = self.get_time_userid_in_data(d)
            id = tu[1]
            if (not self.is_in_user_set(id)):
                continue
            ctn = self.get_content_in_data(d)
            fw = self.filter.has_forbidden_word(ctn)
            if (fw != ''):
                # print(id, ' - 触发过滤词:', fw)
                continue
            filt_res.append(d)

        # 去除<转发微博>
        self.clean_only_repost_data(filt_res)

        # 将</p></br><p>的错误数据，拆分成</p></br>\n<p>
        fixed_res = []
        for d in filt_res:
            while d.find('</p></br><p>') != -1:
                pos = d.find('</p></br><p>')
                left_part = d[:pos+9]
                right_part = d[pos+9:]
                fixed_res.append(left_part)
                d = right_part
            fixed_res.append(d)

        # 全局去重
        tu_map = {}
        for idx in range(0, len(fixed_res)):
            tu = self.get_time_userid_in_data(fixed_res[idx])
            key = tu[0]+'-'+tu[1]
            tu_map[key] = idx
        untapped_res = []
        for k in tu_map.keys():
            untapped_res.append(fixed_res[tu_map[k]])

        # 转发链聚合
        accumulated_res = self.accumulate_multy_repost(untapped_res)
        per = round(len(accumulated_res) / len(data) * 100, 2)
        print('前后数量比较: 原始：', len(data), ' 过滤：', len(filt_res), '修复：', len(fixed_res), ' 去重：', len(untapped_res), ' 合并转发链：', len(accumulated_res), ' 缩水比：', per, '%')
        return accumulated_res

    def clean_only_repost_data(self, data):
        for i in range(len(data)):
            # 内容仅仅是「转发微博」
            data[i] = data[i].replace('<p>转发微博</p>', '').replace('<p>Repost</p>', '')

            # 仅仅写了转发
            if (data[i].find('<p>转发') != -1):
                left = data[i].find('<p>转发')
                right = data[i][left:].find('</p>')
                right += 4
                data[i] = data[i][:left] + data[i][left + right:]

            # 博主无任何表述，仅仅转发
            if (data[i].find('<p>//<a') != -1):
                left = data[i].find('<p>//<a')
                right = data[i][left:].find('</p>')
                right += 4
                data[i] = data[i][:left]+data[i][left+right:]

    # 多人转发同一微博，则聚合
    def accumulate_multy_repost(self, data):
        sptr = WeiboSeperator()
        # 放置seg数据的数组
        seg_list = []
        for w in data:
            seg = sptr.seperate(w)
            seg_list.append(seg)

        # 存放<hash_val, [s_idx]>
        # 将转发同一微博的放到同一个 list 中
        hv_map = {}
        for s_idx in range(len(seg_list)):
            # seg_list[s_idx][-2]指的就是原微博内容，对这一块进行hash计算
            hash_val = hash(seg_list[s_idx][-2])
            # 得到同样hash_val的，就是针对同一内容的不同转发
            _hv = str(hash_val)
            if (hv_map.get(_hv) is None):
                hv_map[_hv] = []
            hv_map[_hv].append(s_idx)

        # 对微博进行聚合
        hv_list = []
        for _hv in hv_map.keys():
            idx_list = hv_map[_hv]
            if (len(idx_list) > 1):
                seg_sequence = []
                # 按照顺序，将seg放入seg_sequence中
                for idx in idx_list:
                    seg_sequence.append(seg_list[idx])
                # 聚合
                big_repost = sptr.accumulate(seg_sequence)
                hv_list.append(big_repost)
            else:
                # idx 对应是 seg_list 的下标，同样也是 data 的下标
                hv_list.append(data[idx_list[0]])

        return hv_list

    # TODO: 同一个作者的几条相似微博，应该取最近的那一条。涉及文本相似度分析。
    # 还有同一博主对同一篇微博分多次转发的

    def is_in_user_set(self, e):
        return e in self.user_set

    def get_time_userid_in_data(self, element):
        if (element.find('(查看原文)') != -1):
            left = element.find('</a>')
            left += 4
        else:
            left = element.find('</span>')
            left += 7
        right = element[left:].find('</p>')
        l = element[left:left + right].split(' ')
        return (l[-2], l[-1])

    def get_content_in_data(self, element):
        left = element.find('</p><p>')
        return element[left+7:]

    def save_result(self, result, file_root, file):
        with open(file_root+'/'+file, 'w') as f:
            for e in result:
                f.write(e+'\n\n')
        print('写文件完成:'+file_root+'/'+file)

def clean(args):
    cleaner = DataCleaner()
    if args.t:
        test()
    elif args.d:
        # 自动填充路径
        dir = args.d
        if dir.find('../') != -1:
            file_below = dir[dir.find('../')+3:]
            dir = os.path.dirname(os.path.abspath(__file__)) + '/export/weibo/group/' + file_below
        cleaner.traverse_directory(dir)
    elif args.a:
        dir = os.path.dirname(os.path.abspath(__file__)) + '/export/weibo/group/'
        cleaner.traverse_directory(dir)
    else:
        file_path = os.path.dirname(os.path.abspath(__file__)) + '/export/weibo/group/'
        now = datetime.now()
        time_str = now.strftime('%Y-%m-%d')
        cleaner.traverse_directory(file_path + str(time_str))

def test():
    cleaner = DataCleaner()
    dir = os.path.dirname(os.path.abspath(__file__)) + '/test_export'
    cleaner.traverse_directory(dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', type=str, default='', help='clean 指定绝对路径的下的数据。也可以简化路径写法，以 ../ 开头，如 -d ../2023-07-16')
    parser.add_argument('-a', action='store_true', help='对全部文件进行处理')
    parser.add_argument('-t', action='store_true', help='执行test')
    args = parser.parse_args()

    clean(args)
