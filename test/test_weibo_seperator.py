from tools.weibo_seperator import WeiboSeperator


class TestWeiboSeperator:

    def test_accumulate(self):
        ws = WeiboSeperator()
        # case 3  转发者+原作者
        print('case3')
        seg_sequence = []
        seg = []
        seg.append('name-1|')
        seg.append('ori-name|')
        seg.append('ori-ctn|')
        seg.append('<>')
        seg_sequence.append(seg)
        seg = []
        seg.append('ori-name|')
        seg.append('ori-ctn|')
        seg.append('<>')
        seg_sequence.append(seg)

        res = ws.accumulate(seg_sequence)
        print(seg_sequence)
        print(res)
        print('')

        # case 2  转发者*n
        print('case2')
        seg_sequence = []
        seg = []
        seg.append('name-1|')
        seg.append('ori-name|')
        seg.append('ori-ctn|')
        seg.append('<>')
        seg_sequence.append(seg)
        seg = []
        seg.append('name-2|')
        seg.append('ori-name|')
        seg.append('ori-ctn|')
        seg.append('<>')
        seg_sequence.append(seg)
        seg = []
        seg.append('name-3|')
        seg.append('cmt-3|')
        seg.append('ori-name|')
        seg.append('ori-ctn|')
        seg.append('<>')
        seg_sequence.append(seg)
        seg = []
        seg.append('name-x|')
        seg.append('ori-name|')
        seg.append('ori-ctn|')
        seg.append('<>')
        seg_sequence.append(seg)

        res = ws.accumulate(seg_sequence)
        print(seg_sequence)
        print(res)
        print('')

        # case-1 转发者*n+原作者
        print('case 1')
        seg_sequence = []
        seg = []
        seg.append('name-1|')
        seg.append('cmt-1|')
        seg.append('ori-name|')
        seg.append('ori-ctn|')
        seg.append('<>')
        seg_sequence.append(seg)
        seg = []
        seg.append('name-2|')
        seg.append('ori-name|')
        seg.append('ori-ctn|')
        seg.append('<>')
        seg_sequence.append(seg)
        seg = []
        seg.append('name-3|')
        seg.append('cmt-3|')
        seg.append('ori-name|')
        seg.append('ori-ctn|')
        seg.append('<>')
        seg_sequence.append(seg)
        seg = []
        seg.append('ori-name|')
        seg.append('ori-ctn|')
        seg.append('<>')
        seg_sequence.append(seg)

        res = ws.accumulate(seg_sequence)
        print(seg_sequence)
        print(res)
        print('')

if __name__ == '__main__':
    tws = TestWeiboSeperator()
    tws.test_accumulate()