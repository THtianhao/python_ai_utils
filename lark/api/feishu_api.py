import io
import json
import os
import time

import requests
from requests_toolbelt import MultipartEncoder

from lark.config import write_config, read_config, image_save_tmp_path
from lark.api.feishu_response import TokenResponse
from lark.api.feishu_user_response import UserResponseData
from image_utils.image_save import download_image, get_file_size

feishu_base_url = "https://open.feishu.cn"
get_access_token = f"{feishu_base_url}/open-apis/auth/v3/tenant_access_token/internal"
get_user_token = f"{feishu_base_url}/open-apis/authen/v1/access_token"
get_pre_code = f"{feishu_base_url}/open-apis/authen/v1/index"
get_refresh_token = f"{feishu_base_url}/open-apis/authen/v1/refresh_access_token"
get_root_token = f"{feishu_base_url}/open-apis/drive/explorer/v2/root_folder/meta"
create_sheet = f"{feishu_base_url}/open-apis/sheets/v3/spreadsheets"
create_doc = f"{feishu_base_url}/open-apis/docx/v1/documents"
upload_image_url = f"{feishu_base_url}/open-apis/drive/v1/medias/upload_all"


class FeishuApi:
    def __init__(self):
        self.tenant_access_token = ""
        self.user_access_token = ""
        self.session = requests.session()
        self.upload = False
        self.session_success = False
        self.config = read_config()

    def check_feishu(self, code, app_id, app_secret):
        response = self.getToken(app_id, app_secret)
        if response is not None:
            if self.config.refresh_token is not None and len(self.config.refresh_token) != 0:
                refreshResult = self.refresh_user_access_token(self.config.refresh_token)
                if refreshResult is not None:
                    self.config.refresh_token = refreshResult.refresh_token
                    write_config(self.config.__dict__)
                    return True
            else:
                userResult = self.get_user_access_token(code)
                if userResult is not None:
                    self.config.refresh_token = userResult.refresh_token
                    write_config(self.config.__dict__)
                    return True
        self.config.refresh_token = ''
        write_config(self.config.__dict__)
        return False

    def update_task_config(self, doc_id, task_id, finish):
        self.config.last_doc = doc_id
        self.config.last_task = task_id
        write_config(self.config.__dict__)
        return False

    def set_upload(self, upload):
        self.upload = upload

    def can_upload(self) -> bool:
        if not self.upload:
            return False
        if not self.session_success:
            return False
        return True

    def getToken(self, app_id, app_secret):
        payload = {"app_id": app_id, "app_secret": app_secret}
        response = self.session.post(url=get_access_token, json=payload)
        if response.status_code == 200:
            dict = json.loads(response.content)
            bean = TokenResponse(**dict)
            if bean.code == 0:
                self.tenant_access_token = bean.tenant_access_token
                print(f"access token = {self.tenant_access_token}")
                return bean
            else:
                print(f"get access token fail")

    def get_tenant_headers(self):
        return {
            "Authorization": f"Bearer {self.tenant_access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }

    def get_user_headers(self):
        return {
            "Authorization": f"Bearer {self.user_access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }

    def get_user_access_token(self, code):
        payload = {
            "grant_type": "authorization_code",
            "code": code
        }
        response = self.session.post(url=get_user_token, headers=self.get_tenant_headers(), json=payload)
        if response.status_code == 200:
            dict = json.loads(response.content)
            if dict['code'] == 0:
                bean = UserResponseData(**dict['data'])
                print(f'new token is {self.user_access_token}')
                self.user_access_token = bean.access_token
                self.session_success = True
                return bean
            else:
                print(f"code= {dict['code']} msg = {dict['msg']}")

    def refresh_user_access_token(self, user_refresh_token):
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": user_refresh_token
        }
        response = self.session.post(url=get_refresh_token, headers=self.get_tenant_headers(), json=payload)
        if response.status_code == 200:
            dict = json.loads(response.content)
            if dict['code'] == 0:
                bean = UserResponseData(**dict['data'])
                self.user_access_token = bean.access_token
                self.session_success = True
                return bean

    def get_root_token(self):
        response = self.session.get(url=get_root_token, headers=self.get_user_headers())
        if response.status_code == 200:
            content = json.loads(response.content)
            if content['code'] == 0:
                root_token = content['data']['token']
                return root_token

    def create_sheet(self, name, root_token):
        payload = {
            "title": name,
            "folder_token": root_token
        }
        response = self.session.post(url=create_sheet, headers=self.get_user_headers(), json=payload)
        if response.status_code == 200:
            content = json.loads(response.content)
            if content['code'] == 0:
                return content['data']['spreadsheet']

    def query_sheetId(self, sheet_token):
        response = self.session.get(
            url=f"{feishu_base_url}/open-apis/sheets/v3/spreadsheets/{sheet_token}/sheets/query",
            headers=self.get_user_headers())
        if response.status_code == 200:
            content = json.loads(response.content)
            if content['code'] == 0:
                return content['data']['sheets'][0]['sheet_id']

    def qut_sheet(self, sheet_token, value):
        response = self.session.put(url=f"{feishu_base_url}/open-apis/sheets/v2/spreadsheets/{sheet_token}/values",
                                    headers=self.get_user_headers(), json=value)
        print(f"qut_sheet = {response.content}")

    def post_image(self, sheet_token, range, image):
        img_bytes = io.BytesIO()
        # 把PNG格式转换成的四通道转成RGB的三通道，然后再保存成jpg格式
        image = image.convert("RGB")
        # 将图片数据存入字节流管道， format可以按照具体文件的格式填写
        image.save(img_bytes, format="JPEG")
        # 从字节流管道中获取二进制
        image_bytes = list(img_bytes.getvalue())
        payload = {
            "range": range,
            "image": image_bytes,
            "name": "demo.png"
        }
        response = self.session.post(
            url=f"{feishu_base_url}/open-apis/sheets/v2/spreadsheets/{sheet_token}/values_image",
            headers=self.get_user_headers(),
            data=json.dumps(payload))
        print(f"post_image = {response.content}")

    def pre_download_image(self, folder_name, url):
        image_folder_path = os.path.join(image_save_tmp_path, folder_name)
        if not os.path.exists(image_folder_path):
            try:
                os.makedirs(image_folder_path)
            except Exception:
                pass
        image_file_path = os.path.join(image_folder_path, os.path.basename(url))
        if not os.path.exists(image_file_path):
            download_image(image_folder_path, url)

    def upload_image(self, folder_name, block_id, url):
        image_folder_path = os.path.join(image_save_tmp_path, folder_name)
        if not os.path.exists(image_folder_path):
            os.makedirs(image_folder_path)
        image_file_path = os.path.join(image_folder_path, os.path.basename(url))
        if not os.path.exists(image_file_path):
            download_image(image_folder_path, url)
        file_size = get_file_size(image_file_path)
        form = {'file_name': 'demo.jpeg',
                'parent_type': "docx_image",
                'parent_node': block_id,
                'size': str(file_size),
                'file': (open(image_file_path, 'rb'))}
        multi_form = MultipartEncoder(form)
        headers = self.get_user_headers()
        headers['Content-Type'] = multi_form.content_type
        response = self.session.post(url=upload_image_url,
                                     headers=headers,
                                     data=multi_form)
        content = json.loads(response.content)
        if response.status_code == 200:
            file_token = content['data']['file_token']
            print(f'file token = {file_token}')
            return file_token

    def create_doc(self, parent_folder, title):
        payload = {
            "folder_token": parent_folder,
            "title": title,
        }
        response = self.session.post(url=f"{feishu_base_url}/open-apis/docx/v1/documents",
                                     headers=self.get_user_headers(),
                                     data=json.dumps(payload))
        document_id = ""
        if response.status_code == 200:
            content = json.loads(response.content)
            if content['code'] == 0:
                document_id = content['data']['document']['document_id']
                return document_id
        print(f"post_image = {response.content} document_id  {document_id}")

    def create_doc_block(self, document_id, block_id, block_type, content):
        desc = {}
        block_text = "text"
        if block_type == 2:
            block_text = "text"
        elif block_type == 3:
            block_text = "heading1"
        elif block_type == 4:
            block_text = "heading2"
        elif block_type == 5:
            block_text = "heading3"
        payload = {
            "index": -1,
            "children": [
                {
                    "block_type": block_type,
                    block_text: {
                        "elements": [
                            {
                                "text_run": {
                                    "content": content,
                                }
                            },
                        ],
                        "style": {}
                    }
                }
            ]
        }
        children = self.request_doc_block(document_id, block_id, payload)
        if children:
            return children[0]['block_id']

    def update_doc_add_grid(self, document_id, block_id):
        payload = {
            "insert_grid_column": {
                "column_index": -1
            }
        }
        response = self.session.patch(
            url=f"{feishu_base_url}/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}",
            headers=self.get_user_headers(),
            data=json.dumps(payload))
        content = response.content
        if response.status_code == 200:
            if content['code'] == 0:
                print("update success")

    def update_doc_block(self, document_id, block_id, image_token):
        payload = {
            "replace_image": {
                "token": image_token
            }
        }
        response = self.session.patch(
            url=f"{feishu_base_url}/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}",
            headers=self.get_user_headers(),
            data=json.dumps(payload))
        content = json.loads(response.content)
        if response.status_code == 200:
            if content['code'] == 0:
                print("update success")

    def create_doc_grid(self, document_id, block_id, grid_count):
        payload = {
            "index": -1,
            "children": [
                {
                    "block_type": 24,
                    "grid": {
                        "column_size": grid_count
                    }
                }
            ]
        }
        children = self.request_doc_block(document_id, block_id, payload)
        block_id = children[0]['block_id']
        block_ids = [child for child in children[0]['children']]
        return block_id, block_ids,

    def create_doc_image(self, document_id, block_id, index=-1):
        payload = {
            "index": index,
            "children": [
                {
                    "block_type": 27,
                    "image": {}
                }
            ]
        }
        children = self.request_doc_block(document_id, block_id, payload)
        if children:
            block_id = children[0]['block_id']
        return block_id

    def request_doc_block(self, document_id, block_id, payload):
        print(f'request doc block id = {block_id} ')
        time.sleep(0.3)
        response = self.session.post(
            url=f"{feishu_base_url}/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children?document_revision_id=-1",
            headers=self.get_user_headers(),
            data=json.dumps(payload))
        new_block_id = ""
        try:
            content = json.loads(response.content)
            if response.status_code == 200:
                if content['code'] == 0:
                    children = content['data']['children']
                    return children
            elif response.status_code == 400:
                print(content)
        except Exception as e:
            print(f"Failed : {e}")
            print("Response content:", response.text, "code = ", response.status_code)

    async def request_doc_block_sync(self, document_id, block_id, payload):
        response = self.session.post(
            url=f"{feishu_base_url}/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children?document_revision_id=-1",
            headers=self.get_user_headers(),
            data=json.dumps(payload))
        new_block_id = ""
        content = json.loads(response.content)
        if response.status_code == 200:
            if content['code'] == 0:
                children = content['data']['children']
                return children
        elif response.status_code == 400:
            print(content)

    def getPreCodeUrl(self):
        return "https://open.feishu.cn/open-apis/authen/v1/index?app_id=cli_a483ea8b94e3100e&redirect_uri=http://127.0.0.1"
