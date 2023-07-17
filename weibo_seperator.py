
# 微博内容分离+聚合器，根据<p></p>进行分块
# seg[-1]永远是</br>
class WeiboSeperator:
    def seperate(self, data):
        content = data

        seg = []
        while (True):
            if (content.find('<p>') != -1):
                left = content.find('<p>')
                right = content.find('</p>')
                right += 4
                e = content[left:right]
                seg.append(e)
                content = content[right:]
                continue
            if (content.find('</br>') != -1):
                break
        seg.append('</br>')
        return seg

    def accumulate(self, seg_sequence):
        big_repost = ''
        # 取每条微博的转发链
        for i in range(len(seg_sequence)-1):
            seg = seg_sequence[i]
            l = seg[:-3] # 取转发的[转发人,评论]内容
            if (len(l) == 1):
                if (i == 0):
                    s = ''.join(l[0])
                else:
                    s = ''
            else:
                s = ''.join(l)
            big_repost = big_repost + s

        last = seg_sequence[-1] # 取最后一个seg
        big_repost = big_repost + ''.join(last[-3:]) # 与末尾3个<p></p>拼接
        return big_repost

if __name__ == '__main__':
    # content = '''<p><span style="color:red;">宝玉xp</span><a href="https://m.weibo.cn/status/4922786381827478">(查看原文)</a> 2023-07-12 21:06:37 1727858283</p><p><span style="color:green;">转发了 </span><span style="color:red;">宝玉xp</span> 2023-07-12 12:22:54</p><p>去年的AIGC当红炸子鸡估值15亿美元的AI文案创作公司Jasper裁员了 </p></br>'''
    # ws = WeiboSeperator()
    # seg = ws.seperate(content)
    # for e in seg:
    #     print(e)


    seg_list = []
    for i in range(1, 4):
        seg = []
        seg.append('<p>姓名' + str(i) +'</p>')
        # seg.append('<p>评论内容' + str(i) + '</p>')
        seg.append('<p>origin name</p>')
        seg.append('<p>origin content</p>')
        seg.append('</br>')

        seg_list.append(seg)

    ws = WeiboSeperator()
    big_repost = ws.accumulate(seg_list)
    print(big_repost)