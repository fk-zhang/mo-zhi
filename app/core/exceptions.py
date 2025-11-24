from __future__ import annotations

"""
统一异常处理与响应构建。

本模块提供：
- _build_error_response：将错误信息规范化为 JSON 响应。
- setup_exception_handlers：注册 FastAPI 级别的异常处理器（HTTP、校验、未处理异常）。
"""

from typing import Any

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .logging import get_logger

logger = get_logger(__name__)


def _build_error_response(
    message: str,
    status_code: int,
    error_code: str | None = None,
    details: Any | None = None,
) -> JSONResponse:
    """构建统一的错误响应体。

    参数：
    - message：错误提示信息（展示给调用方）。
    - status_code：HTTP 状态码。
    - error_code：业务错误码（可选）。
    - details：错误详情（用于调试/参数校验信息）。

    返回：
    - JSONResponse：带有标准字段的 JSON 响应。
    """
    payload: dict[str, Any] = {
        "success": False,
        "message": message,
        "error_code": error_code or str(status_code),
    }
    if details is not None:
        payload["details"] = details
    return JSONResponse(status_code=status_code, content=payload)


def setup_exception_handlers(app) -> None:
    """注册全局异常处理器。

    包含三类处理：
    - HTTPException：直接返回对应状态码与信息。
    - RequestValidationError：422 参数校验错误，返回错误列表。
    - Exception：兜底处理，返回 500。
    """
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.warning(
            f"HTTPException: {exc.status_code} {exc.detail} path={request.url.path}"
        )
        return _build_error_response(
            message=str(exc.detail) if exc.detail else "HTTP error",
            status_code=exc.status_code,
            error_code="HTTP_EXCEPTION",
        )

    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        logger.warning(f"ValidationError: {exc.errors()} path=={request.url.path}")
        return _build_error_response(
            message="Validation error",
            status_code=422,
            error_code="VALIDATION_ERROR",
            details=exc.errors(),
        )

    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.error(
            f"Unhandled Exception at {request.url.path}: {exc}",
            exc_info=True,
        )
        return _build_error_response(
            message="Internal server error",
            status_code=500,
            error_code="INTERNAL_SERVER_ERROR",
        )

    # 将处理器注册到 FastAPI 实例
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
