import lark_oapi as lark
from lark_oapi.api.im.v1 import ListChatRequest


class LarkServerApi:
    def __init__(self, appid, app_secret):
        self.client = lark.Client.builder().\
            app_id(appid).app_secret(app_secret).build()

    def read_im_list(self):
        req = ListChatRequest().builder().build()
        resp = self.client.im.v1.chat.list(req)
        chat_ids = []
        if resp.code == 0:
            for chat in resp.data.items:
                chat_ids.append(chat.chat_id)
        print(chat_ids)
        return chat_ids

    def send_im_message(self):
        pass


