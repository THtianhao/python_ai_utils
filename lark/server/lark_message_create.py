import json

import lark_oapi

from crawler.core import CodeWithPaperContent

def create_card_message(bean_list: list[CodeWithPaperContent]):
    message = {
        "type": "template",
        "data": {
            "template_id": "AAqC9L93wQZRI",
            "SendImageRequest": "1.0.1",
            "template_variable": {
                "object_list_1": [
                ]
            }
        }
    }
    for bean in bean_list:
       content = f"""<font color='red'>**{bean.title}**</font> <text_tag color="blue">{bean.categorie}</text_tag>
{bean.description}
[**paper**]({bean.paper_link}) / [github]({bean.code_link}) (⭐️<font color='yellow'>**{bean.stars_count}**</font>) (<font color='green'>**{bean.stars_per_hour}⭐️ / hour**</font>) """
       message["data"]["template_variable"]["object_list_1"].append({"content": content})
    json_str = lark_oapi.JSON.marshal(message)
    # result = json_str.replace('"', '\\"')
    return json_str
