import logging
from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import QueuePool
from sqlalchemy import event, text
from sqlalchemy.exc import SQLAlchemyError

from .config import settings

logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

# Create engine with connection pooling
engine = create_async_engine(
    settings.database_url,
    echo=settings.sqlalchemy_echo,
    poolclass=QueuePool,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_timeout=settings.db_pool_timeout,
    pool_recycle=settings.db_pool_recycle,
    pool_pre_ping=settings.db_pool_pre_ping,
)

# Configure session factory with additional options
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

# Add connection pool event listeners
@event.listens_for(engine.sync_engine, 'checkout')
def on_checkout(dbapi_connection, connection_record, connection_proxy):
    """Called when a connection is retrieved from the pool."""
    logger.debug("Connection checked out from pool")

@event.listens_for(engine.sync_engine, 'checkin')
def on_checkin(dbapi_connection, connection_record):
    """Called when a connection is returned to the pool."""
    logger.debug("Connection returned to pool")

@event.listens_for(engine.sync_engine, 'connect')
def on_connect(dbapi_connection, connection_record):
    """Called when a new database connection is created."""
    logger.debug("New database connection established")

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async DB session with connection pooling.
    
    Usage:
        @router.get("/")
        async def some_endpoint(session: AsyncSession = Depends(get_session)):
            # Use the session
            result = await session.execute(text("SELECT 1"))
            return {"status": "ok"}
    """
    session: Optional[AsyncSession] = None
    try:
        session = AsyncSessionLocal()
        yield session
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        if session:
            await session.rollback()
        raise
    finally:
        if session:
            await session.close()


async def db_simple_check() -> bool:
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT 1"))
        return result.scalar() == 1


