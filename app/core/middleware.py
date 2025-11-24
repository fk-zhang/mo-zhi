from fastapi.middleware.cors import CORSMiddleware

"""
跨域（CORS）中间件配置。

为 FastAPI 应用统一开启跨域访问，便于前端从不同域名调用后端接口。
"""

def setup_cors(app):
    """为应用添加 CORS 中间件。

    说明：
    - allow_origin_regex=".*"：允许任意来源（可按需收紧域名）。
    - allow_credentials=True：允许携带 Cookie 等凭证。
    - allow_methods/headers=["*"]：放开所有方法与请求头。
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=".*",  # 放开所有来源
        allow_credentials=True,
        allow_methods=["*"],      # 放开所有方法
        allow_headers=["*"]       # 放开所有请求头
    )