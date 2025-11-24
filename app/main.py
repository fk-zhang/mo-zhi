from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends    

from .api.router import api_router
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from .core.session import get_session, Base, engine
from .core.exceptions import setup_exception_handlers
from .core.middleware import setup_cors
from . import models  # 这行确保所有模型已被导入注册

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Database tables created successfully")

        yield
    except Exception as e:
        print(f"Error in lifespan: {e}")
        pass
    finally:
        await engine.dispose()

app = FastAPI(title="mo-zhi-backend-api", lifespan=lifespan)

# 注册全局异常
setup_exception_handlers(app)
# 注册跨域中间件
setup_cors(app)

# include api routes
app.include_router(api_router)


@app.get("/health", tags=["system"])
async def health():
    return {"status": "ok", "message": "Backend API is running"}

@app.get("/", tags=["system"])
async def docs():
    return {"message": "Welcome to mo-zhi API", "docs": "/docs"}

@app.get("/db/check", tags=["system"])
async def db_check(session: AsyncSession = Depends(get_session)):
    result = await session.execute(text("SELECT 1"))
    ok = result.scalar() == 1
    return {"db": "ok" if ok else "fail"}
