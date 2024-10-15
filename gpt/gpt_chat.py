# import the OpenAI Python library for calling the OpenAI API
import traceback

from openai import OpenAI
import os

from pydantic import BaseModel

from .gpt_utils import get_message_by_history
from python_ai_utils.lark.alarm.lark_alarm import LarkAlarm
from python_ai_utils.lark.alarm.lark_api import send_alert_to_feishu

class ResponseModel(BaseModel):
    content: str

class GPTChat:
    def __init__(self, key):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", key))
        # MODEL = "gpt-3.5-turbo"
        # MODEL = "gpt-4o"
        self.MODEL = "gpt-4o-mini"

    def chat_complete(self, system, history, first_is_me=True, is_history_format=False, lark_alarm: LarkAlarm = None):
        messages = get_message_by_history(system, history, first_is_me, is_history_format)
        response = self.client.chat.completions.create(
            model=self.MODEL,
            messages=messages,
            temperature=0.7,
            top_p=0.9,
        )
        content = response.choices[0].message.content
        if lark_alarm is not None and content is None or content == "":
            content = ''
            stack_list = traceback.format_stack()
            stack_str = ''.join(stack_list)
            response_json = response.dict()
            send_message = f'语言模型错误:\n堆栈信息\n{stack_str}\n\nresponse信息\n{response_json}'
            LarkAlarm.notify(send_message)
        return content
