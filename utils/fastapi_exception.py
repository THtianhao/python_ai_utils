import http
import json
import traceback

from starlette.requests import Request
from starlette.responses import JSONResponse

from python_ai_utils.lark.alarm.lark_api import send_alert_to_feishu


def error_in_file(app, log_tool, lark_webhook_url=None):
    @app.middleware("http")
    async def save_request_body(request: Request, call_next):
        body = await request.body()
        decode_body = body.decode()
        try:
            request.state.body = json.dumps(json.loads(decode_body))
        except json.JSONDecodeError:
            request.state.body = None
        response = await call_next(request)
        return response

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, e: Exception):
        log_tool.error(f"======================exception========================")
        path = request.url.path
        headers_dict = dict(request.headers)
        headers = json.dumps(headers_dict)
        query_params_dict = dict(request.query_params)
        query_params = json.dumps(query_params_dict)
        try:
            body = getattr(request.state, 'body', None)
        except Exception:
            body = None
        error_message = f"请求路径: {path}\n请求头: {headers}\n请求查询参数: {query_params}\n请求体: {body}"
        log_tool.error(error_message)
        log_tool.error(f"{e}", exc_info=True)
        if lark_webhook_url:
            error_message_with_stack = error_message + f"错误信息: {str(e)}\n 堆栈信息: {traceback.format_exc()}"
            send_alert_to_feishu(lark_webhook_url, error_message_with_stack)
        return JSONResponse(
            status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"message": str(e)},
        )
