
class Page:
    def __init__(self, winfo_list, previous_cursor, next_cursor, max_id):
        self.winfo_list = winfo_list
        self.previous_cursor = previous_cursor
        self.next_cursor = next_cursor
        self.max_id = max_id

    def get_raw_last_created_at(self):
        farest_winfo = self.winfo_list[-1]
        return farest_winfo.created_at