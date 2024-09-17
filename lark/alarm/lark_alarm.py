from python_ai_utils.lark.alarm.lark_api import send_alert_to_feishu


class LarkAlarm:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def notify(self, alert_message: str) -> None:
        send_alert_to_feishu(self.webhook_url, alert_message)