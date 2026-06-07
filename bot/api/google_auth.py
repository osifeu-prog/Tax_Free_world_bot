from fastapi import APIRouter, HTTPException
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from pydantic import BaseModel
from bot.database.models import User
from bot.database.session import async_session
from bot.utils.auth import create_access_token
from sqlalchemy import select

router = APIRouter()
GOOGLE_CLIENT_ID = "123456789-xxxxxx.apps.googleusercontent.com"

class GoogleAuthRequest(BaseModel):
    credential: str
    telegram_id: int | None = None

@router.post("/auth/google")
async def google_auth(data: GoogleAuthRequest):
    try:
        info = id_token.verify_oauth2_token(data.credential, google_requests.Request(), GOOGLE_CLIENT_ID)
    except ValueError:
        raise HTTPException(400, "Invalid Google token")
    google_id = info["sub"]
    email = info.get("email")
    async with async_session() as session:
        stmt = select(User).where(User.google_id == google_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            user = User(google_id=google_id, email=email, language="he")
            session.add(user)
            await session.commit()
        if data.telegram_id and user.telegram_id != data.telegram_id:
            user.telegram_id = data.telegram_id
            await session.commit()
        token = create_access_token({"sub": str(user.id), "email": email})
        return {"access_token": token, "user_id": user.id}
