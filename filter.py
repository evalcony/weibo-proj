import os

class Filter:
    # 允许的user_id列表
    def __init__(self):
        self.forbidden_words = self.read_forbidden_words_config()

    def read_forbidden_words_config(self):
        words = []
        root_dir = os.path.dirname(os.path.abspath(__file__))
        with open(root_dir+'/forbidden_words.txt', 'r') as file:
            for word in file:
                words.append(word.replace("\n",""))
        return words

    def has_forbidden_word(self, text):
        for word in self.forbidden_words:
            if word in text:
                return word
        return ''

if __name__ == '__main__':
    filter = Filter()
    print(filter.forbidden_words)