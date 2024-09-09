import http
import json
from starlette.requests import Request
from starlette.responses import JSONResponse


def error_in_file(app, log_tool):
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
        log_tool.error(f"请求路径: {path}")
        log_tool.error(f"请求头: {headers}")
        log_tool.error(f"请求查询参数: {query_params}")
        log_tool.error(f"请求体: {body}")
        log_tool.error(f"{e}", exc_info=True)
        return JSONResponse(
            status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"message": str(e)},
        )
