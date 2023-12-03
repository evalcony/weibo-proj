
# import sys
# sys.path.append('../..')
import utils


class MtdInfo:
    def __init__(self, item):
        self.created_at = item["created_at"]
        self.id = item["id"]
        self.url = item["url"]
        self.content = item["content"]
        self.account = Account(item['account'])
        self.reblog = False

        self.media_attachments = self._get_media(item)

        if item['reblog'] is not None:
            reblog = item['reblog']
            self.reblog_content = reblog['content']
            self.reblog_account = Account(reblog['account'])
            self.reblog = True

    def _get_media(self, item):
        medias = item['media_attachments']
        attachments = []
        for m in medias:
            attachments.append(m['url'])
        return attachments
    def as_mastodon(self):
        # 处理有图片的帖子
        if self.media_attachments != []:
            return self._media_t()

        if not self.reblog:
            t = """
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

    def _media_t(self):

        media_html = ""
        for m in self.media_attachments:
            path = 'medias/'+m.split('/')[-1]
            img_html = '<img src="{}"/>'.format(path)
            media_html = media_html+img_html
        t = """
{} {} {}</br>
{}</br>
{}
</br>
""".format(self.account.display_name, self.account.id, utils.format_time2(self.created_at),
                   self.content, media_html)
        return t


class Account:
    def __init__(self, account):
        self.id = account['id']
        self.username = account['username']
        self.display_name = account['display_name']
