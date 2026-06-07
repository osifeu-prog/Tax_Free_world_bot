from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
import qrcode, io, os

router = Router()

@router.message(Command("qr"))
async def cmd_qr(msg: Message):
    from bot.database.session import async_session
    from bot.database.models import Referral
    from sqlalchemy import select

    # מצא או צור קוד הפניה
    async with async_session() as session:
        stmt = select(Referral).where(Referral.inviter_id == msg.from_user.id)
        ref = (await session.execute(stmt)).scalar_one_or_none()
        if not ref:
            import random, string
            code = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            ref = Referral(code=code, inviter_id=msg.from_user.id, clicks=0)
            session.add(ref)
            await session.commit()
        ref_link = f"https://t.me/Tax_Free_world_bot?start=ref{ref.code}"

    # צור QR
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(ref_link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)

    await msg.answer_photo(
        BufferedInputFile(buf.read(), filename='qr.png'),
        caption=f"🔗 קישור הפניה שלך:\n{ref_link}\n\nשתף את הקוד וגרוף נקודות!"
    )
