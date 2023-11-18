
import argparse
import os
import time

import total_text_filler
import utils

# DEFAULT_WEIBO_EXPORT_PATH = '/export/weibo/group/'
DEFAULT_WEIBO_EXPORT_PATH = '/test_export/' # 文件的路径前缀

# 处理历史长微博数据
def history_longtext(args):
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
    elif args.t:
        test_case()

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

                    # 睡眠
                    sleep_time = utils.random_num(1, 15)
                    print(f'wait {sleep_time}s......')
                    time.sleep(sleep_time)

def processor(filename):
    lines = utils.read_dirpath_file(filename) # 读取绝对路径

    for i in range(len(lines)):
        line = lines[i]
        if line.find('全文</a>') != -1:
            tup = get_lid_text(line)
            lid = tup[0]
            text = tup[1]
            total_text = total_text_filler.totalize_text(lid, text)
            lines[i] = line.replace(text, total_text)
    utils.write_dirpath_file(filename, lines)

def get_lid_text(line):
    l_line = len(line)
    R_AHREF = 'ferh a<' # <a href
    l_R_AHREF = len(R_AHREF)
    p = line.find('全文</a>')
    q = reverse(line).find(R_AHREF)
    s_href = q+l_R_AHREF
    rline = reverse(line)

    # 提取id部分
    # print(line[len(line)-href_start:])
    endpart = line[l_line-s_href:]
    s_id = endpart.find('status/')
    e_id = endpart[s_id+len('status/'):].find('"')
    id = endpart[s_id+len('status/'):s_id+len('status/')+e_id]
    # print(id)

    # 提取text部分
    s_text = rline.find('>p<')
    e_text = p+len('全文</a>')
    # print(line[l_line-s_text:e_text])
    return (id, line[l_line-s_text:e_text])

def reverse(string):
    return "".join(reversed(string))


def test_case():
    # get_lid_text('<p><span style="color:red;">旧常识</span><a href="https://m.weibo.cn/status/4963032939890143">(查看原文)</a> 2023-10-31 22:32:04 5822404600</p><p>“人际的共同行为预期是道德判断的一个事·实·背景。良法通过构造出行为预期，构造了对罪·恶·的·归·责·，区分了有道德污点的与清白无辜的行为。恶法也会构造出行为预期，并同时构造了对违法善行的功·绩·的·归·因·，原本只是正常的行为在恶法下成了英雄壮举。”</p><p><span style="color:red;">旧常识</span><a href="https://m.weibo.cn/status/4963003259945266">(查看原文)</a> 2023-10-31 20:34:07 5822404600</p><p>《生活世界中的功利主义》<br /><br />这三页谈的是功利主义与义务论的 “责任域” 差异。义务论的责任领域是被直言律令划分的，例如 “不可说谎” 的责任域就只是当下行为不可说谎，至于导致你的朋友被杀则不是你的责任。而功利主义的责任域，取决于行为的效用确定性，确定性越高则越是必须被纳入功利考量。或者 ...<a href="https://m.weibo.cn/status/4963003259945266">全文</a></p></br>')
    # get_lid_text('<p><span style="color:red;">冰曦微语</span> 2023-04-01 09:44:59 1105989411</p><p><span style="color:green;">转发了 </span><span style="color:red;">中国妇女报</span> 2023-03-31 18:10:59</p><p>【男女足实现“同工同酬”有多难】根据国际足联的计划，今年女足世界杯的总奖金将提升至1.52亿美元。但相比去年男足世界杯4.4亿美元的总奖金仍差距明显。近年来，随着世界女足运动尤其是欧洲职业女足的不断发展，国际足坛呼吁男女足“同工同酬”的声音越来越响亮。但“足球产业内并非所有人都认同。男 ...<a href="https://m.weibo.cn/status/4885416233142948">全文</a></p></br>')
    # get_lid_text('<p><span style="color:red;">冰曦微语</span><a href="https://m.weibo.cn/status/4963019639756265">(查看原文)</a> 2023-10-31 21:39:13 1105989411</p><p>【马啸｜地方发展中的“条赋块能”：基于铁路的案例研究】条块关系是中国政治运行中的一个重要概念。既有研究多关注条块之间的功能差异与张力，对于条块间可能存在的合作与赋能关系着墨不多。文章提出，当“条”所提供的公共物品存在明确的次国家边界，特别是当其嵌入作为“块”的地方政府辖区时（如铁 ...<a href="https://m.weibo.cn/status/4963019639756265">全文</a></p></br>')
    # get_lid_text('<p><span style="color:red;">新京报书评周刊</span> 2023-04-01 15:30:07 1047467705</p><p>【《血色要塞》：一场从未真正结束的围城之战】令人唏嘘的是，“一战”结束后，被权力之手轻率放出的恶魔，仍在帝国的废墟之上游荡，无情地操弄、践踏着生命。“最可怕的是，帝国解体了，但暴力仍然在持续、变异并进一步激化。”普热梅希尔的悲剧不会真正落幕，因为，文明永远无法承受恶魔的试炼。  ...<a href="https://m.weibo.cn/status/4885738137060851">全文</a></p></br>')
    # 暂无查看权限
    tup = get_lid_text(
        '<p><span style="color:red;">冰曦微语</span><a href="https://m.weibo.cn/status/4948853797686875">(查看原文)</a> 2023-09-22 19:29:13 1105989411</p><p>【林泽杰：唐节愍太子平反案与史官的认知变迁】是否应该为节愍太子平反，史家争论不休。唐睿宗时期，韦凑上《论谥节愍太子疏》，反对赠予李重俊“节愍”谥号，公案肇起。有唐一代，基本上对节愍太子及其谥号保持“接纳”态势。到两宋时期，受义理史学影响，欧阳修、朱熹等学者进一步肯定节愍太子的行为 ...<a href="https://m.weibo.cn/status/4948853797686875">全文</a></p></br>')
    id = tup[0]
    text = tup[1]
    total_text = total_text_filler.totalize_text(id, text)
    print(total_text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', type=str, default='',
                        help='指定绝对路径的下的数据。也可以简化路径写法，以 ../ 开头，如 -d ../2023-07-16 其中，../ 表示省略路径之前的部分')
    parser.add_argument('-a', action='store_true', help='对全部文件进行处理')
    parser.add_argument('-t', action='store_true', help='执行test')
    args = parser.parse_args()

    history_longtext(args)


