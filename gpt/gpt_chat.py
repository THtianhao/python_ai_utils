# import the OpenAI Python library for calling the OpenAI API
from openai import OpenAI
import os

from pydantic import BaseModel

from gpt_utils import get_message_by_history


class ResponseModel(BaseModel):
    content: str


class GPTChat:
    def __init__(self, key):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", key))
        # MODEL = "gpt-3.5-turbo"
        # MODEL = "gpt-4o"
        self.MODEL = "gpt-4o-mini"

    def chat_complete(self, system, history, first_is_me=True, is_history_format=False):
        messages = get_message_by_history(system, history, first_is_me, is_history_format)
        response = self.client.chat.completions.create(
            model=self.MODEL,
            messages=messages,
            temperature=0.7,
            top_p=0.9,
        )
        content = response.choices[0].message.content
        return content
