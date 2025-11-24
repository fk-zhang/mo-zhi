import time
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")

class Response(BaseModel, Generic[T]):
    success: bool = True
    code: int = 0
    message: str = "success"
    result: Optional[T] = None
    timestamp: int = int(round(time.time() * 1000))

    @classmethod
    def ok(cls, result: Optional[T] = None, message: str = "success") -> "Response[T]":
        return cls(result=result, message=message)

    @classmethod
    def failed(cls, message: str = "fail", code: int = 1, result: Optional[T] = None) -> "Response[T]":
        return cls(success=False, code=code, message=message, result=result)