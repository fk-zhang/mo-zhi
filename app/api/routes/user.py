from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...core.session import get_session
from ...models.user import User
from ...core.response import Response


router = APIRouter(prefix="/users", tags=["users"])


@router.get("")
async def list_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    data = [{"id": u.id, "name": u.name} for u in users]
    return Response.ok(result=data)

