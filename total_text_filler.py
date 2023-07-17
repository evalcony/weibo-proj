
def totalize_text(text):
    base_url = 'https://m.weibo.cn/'

    # <a href="/status/4884565010943284">全文</a>
    if text.endswith('全文</a>'):
        href = ''
        # get_single_total_weibo(href)
        new_text = text.replace('/status/', base_url + 'status/')
        return new_text
    return text