import lark_oapi

def create_card_message_from_template(template_id: str, version: str, variables: dict):
    message = {
        "type": "template",
        "data": {
            "template_id": template_id,
            "template_version_name": version,
            "template_variable": variables
        }
    }
    return lark_oapi.JSON.marshal(message)
