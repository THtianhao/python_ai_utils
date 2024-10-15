import requests

class LarkAlarm:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_alert_to_feishu(self, webhook_url, alert_message):
        headers = {
            "Content-Type": "application/json"
        }
        # 创建要发送的消息内容
        data = {
            "msg_type": "text",  # 消息类型，这里是文本消息
            "content": {
                "text": alert_message  # 警报消息内容
            }
        }
        # 发送 POST 请求到飞书 Webhook
        response = requests.post(webhook_url, headers=headers, data=json.dumps(data))

        # 打印返回结果
        if response.status_code == 200:
            print("警报发送成功")
        else:
            print(f"警报发送失败: {response.status_code}, {response.text}")

    def notify(self, alert_message: str) -> None:
        self.send_alert_to_feishu(self.webhook_url, alert_message)
