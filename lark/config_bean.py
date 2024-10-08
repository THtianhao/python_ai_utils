from dataclasses import dataclass

class ConfigBean:
    def __init__(self, port="", host="", task_path="", operation=1, upload_feishu=2, feishu_code="", refresh_token="", at_email="", last_doc="", last_task=""):
        self.port: str = port
        self.host: str = host
        self.task_path: str = task_path
        self.operation: int = operation  # 1为merge+ txt2Img 2为 merge
        self.upload_feishu: int = upload_feishu  # 1 上传 2 不上传
        self.feishu_code: str = feishu_code
        self.refresh_token: str = refresh_token
        self.at_email: str = at_email
        self.last_doc: str = last_doc
        self.last_task: str = last_task
