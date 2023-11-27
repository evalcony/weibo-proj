import re
import sys

sys.path.append('..')
import utils

class Filter:
    def __init__(self):
        self.forbidden_words = self.read_forbidden_words_config()

    def read_forbidden_words_config(self):
        words = []
        root_dir = utils.file_path('config/forbidden_words.txt')
        print(root_dir)
        with open(root_dir, 'r') as file:
            for word in file:
                words.append(word.replace("\n",""))
        return words

    def has_forbidden_word(self, text):

        # 如果微博长度超过300，则对屏蔽词放行
        # 300 是一个经验值，可以调整
        if len(self.pure_text(text)) > 300:
            return ''

        for word in self.forbidden_words:
            if word in text:
                return word
        return ''

    # 纯内容长度
    def pure_text(self, text):
        """去除文本中的 HTML 标签"""
        # 匹配所有 HTML 标签的正则表达式
        pattern = re.compile(r"<[^>]+>", re.DOTALL)
        # 将文本中的 HTML 标签替换为空字符串
        return re.sub(pattern, "", text)

    # todo
    # user_id 白名单列表

if __name__ == '__main__':
    filter = Filter()
    print(filter.forbidden_words)