import os
import sys

from typing import List

from alibabacloud_devops20210625.client import Client as devops20210625Client
from alibabacloud_devops20210625.models import ListWorkitemsRequest, ListWorkitemsResponseBodyWorkitems, \
    GetWorkItemInfoResponseBodyWorkitem
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class CodeUpClient:
    def __init__(self, access_key_id: str, access_key_secret: str, org_id: str, word_id: str):
        config = open_api_models.Config(
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
            access_key_id=access_key_id,
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
            access_key_secret=access_key_secret
        )
        config.endpoint = f'devops.cn-hangzhou.aliyuncs.com'
        self.client = devops20210625Client(config)
        self.org_id = org_id
        self.work_id = word_id

    def get_item_list(self, conditions) -> list[ListWorkitemsResponseBodyWorkitems] | None:
        headers = {}
        try:
            request = ListWorkitemsRequest(
                category="Req",
                conditions=conditions,
                space_type="Project",
                space_identifier=self.work_id,

            )
            runtime = util_models.RuntimeOptions()
            headers = {}
            response = self.client.list_workitems_with_options(self.org_id, request, headers, runtime)
            if response.status_code == 200:
                return response.body.workitems
        except Exception as error:
            print(error.message)
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)

    def get_item_info(self, item_id) -> GetWorkItemInfoResponseBodyWorkitem | None:
        try:
            response = self.client.get_work_item_info(self.org_id, item_id)
            if response.status_code == 200:
                return response.body.workitem
        except Exception as error:
            print(error.message)
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)

    @staticmethod
    async def main_async(self, args: List[str], ) -> None:
        headers = {}
        try:
            # 复制代码运行请自行打印 API 的返回值
            await self.client.skip_pipeline_job_run_with_options_async('your_value', '1', '', '', headers,
                                                                       util_models.RuntimeOptions())
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)
