from fastapi import Depends
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

async def get_current_user(db: AsyncSession = Depends(get_db)):
    # Dummy — can be extended later
    return {"msg": "current user"}

