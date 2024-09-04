import lark_oapi as lark
from lark_oapi.api.im.v1 import ListChatRequest, CreateMessageRequestBody, CreateMessageRequest

class LarkServerApi:
    def __init__(self, appid, app_secret):
        self.client = lark.Client.builder().app_id(appid).app_secret(app_secret).build()

    def read_im_list(self) -> list[str]:
        req = ListChatRequest().builder().build()
        resp = self.client.im.v1.chat.list(req)
        chat_ids = []
        if resp.code == 0:
            for chat in resp.data.items:
                chat_ids.append(chat.chat_id)
        return chat_ids

    def send_im_message(self, group_id, content):
        request_body = CreateMessageRequestBody. \
            builder(). \
            msg_type("interactive"). \
            receive_id(group_id). \
            content(content).build()
        request = CreateMessageRequest.builder().request_body(request_body).receive_id_type("chat_id").build()
        resp = self.client.im.v1.message.create(request)
        if resp.code == 0:
            print("success", resp)
        pass
