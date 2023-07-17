import total_text_filler
from user import User

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
        self.text = total_text_filler.totalize_text(self.text)
