from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select
from bot.services.translation_service import translator

router = Router()

async def get_user_lang(uid: int) -> str:
    async with async_session() as s:
        u = (await s.execute(select(User).where(User.telegram_id == uid))).scalar_one_or_none()
        return u.language if u and u.language else "he"

@router.message(Command("qr"))
async def cmd_qr(msg: Message):
    lang = await get_user_lang(msg.from_user.id)
    from bot.database.session import async_session as s2
    from bot.database.models import Referral
    from sqlalchemy import select as sel
    import random, string, qrcode, io
    async with s2() as session:
        stmt = sel(Referral).where(Referral.inviter_id == msg.from_user.id)
        ref = (await session.execute(stmt)).scalar_one_or_none()
        if not ref:
            code = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            ref = Referral(code=code, inviter_id=msg.from_user.id, clicks=0)
            session.add(ref)
            await session.commit()
        link = f"https://t.me/Tax_Free_world_bot?start=ref{ref.code}"
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    caption = translator.t(lang, "qr_caption") + f"\n{link}"
    await msg.answer_photo(photo=BufferedInputFile(buf.read(), 'qr.png'), caption=caption)
