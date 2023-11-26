from data.weibo import total_text_filler
from data.weibo.user import User

class RetweetedStatus:
    def __init__(self, rs_json):
        self.created_at = rs_json['created_at']
        self.id = rs_json['id']
        self.text = rs_json['text']
        u = rs_json['user']
        if u != None:
            self.user = User(u['id'], u['screen_name'])
        else:
            self.user = User(0, '')
        try:
            self.is_long_text = rs_json['isLongText']
        except:
            print('捕获异常 ' + str(self.created_at) + ' wid:' + str(self.id) + ' text:' + str(self.text) + ' uid:' + str(self.user.id) + ' uname:' + str(self.user.screen_name))
            self.is_long_text = False
        if self.is_long_text:
            self.text = total_text_filler.totalize_text(self.id, self.text)
