import utils


class MtdInfo:
    def __init__(self, item):
        self.created_at = item["created_at"]
        self.id = item["id"]
        self.url = item["url"]
        self.content = item["content"]
        self.account = Account(item['account'])
        self.reblog = False
        if item['reblog'] is not None:
            reblog = item['reblog']
            self.reblog_content = reblog['content']
            self.reblog_account = Account(reblog['account'])
            self.reblog = True

    def as_mastodon(self):
        if not self.reblog:
            t ="""
{} {} {}</br>
{}</br>
</br>
""".format(self.account.display_name, self.account.id, utils.format_time2(self.created_at),
                    self.content)
        else:
            t = """
{} {} 转发了 {} {}</br>
{}</br>
</br>
""".format(self.account.display_name, self.account.id, self.reblog_account.display_name, utils.format_time2(self.created_at),
                    self.reblog_content)
        return t


class Account:
    def __init__(self, account):
        self.id = account['id']
        self.username = account['username']
        self.display_name = account['display_name']
