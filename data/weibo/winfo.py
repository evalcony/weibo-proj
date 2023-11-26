# 指代单个微博
from data.weibo import total_text_filler
import utils

class Winfo:
    def __init__(self, created_at, id, text, user, retweeted_status=None, is_long_text=False):
        self.created_at = created_at
        self.id = id
        self.text = text
        self.user = user
        self.retweeted_status = retweeted_status
        self.has_retweeted = self.retweeted_status != None
        self.is_long_text = is_long_text

        if is_long_text:
            self.text = total_text_filler.totalize_text(self.id, self.text)

    def __str__(self):
        return "Winfo: created_at:{} id:{} text:{} user.id:{} user.screen_name:{} retweeted_status:{}".format(
            self.created_at, self.id, self.text, self.user.id, self.user.screen_name, self.retweeted_status
        )

    def as_weibo(self):
        rs = self.retweeted_status
        if rs:
            rs_user = rs.user
            w = """
<p><span style="color:red;">{}</span><a href="https://m.weibo.cn/status/{}">(查看原文)</a> {} {}</p>
<p>{}</p>
<p><span style="color:green;">转发了 </span><span style="color:red;">{}</span> {}</p>
<p>{}</p></br>
""".format(self.user.screen_name, self.id, utils.format_time(self.created_at), self.user.id, self.text,
                       rs_user.screen_name, utils.format_time(rs.created_at), rs.text)
        else:
            w = """
<p><span style="color:red;">{}</span><a href="https://m.weibo.cn/status/{}">(查看原文)</a> {} {}</p>
<p>{}</p></br>
""".format(self.user.screen_name, self.id, utils.format_time(self.created_at), self.user.id, self.text)
        return w