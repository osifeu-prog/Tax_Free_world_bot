from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.services.translation_service import translator
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select

router = Router()

async def get_user_lang(telegram_id: int) -> str:
    async with async_session() as session:
        stmt = select(User).where(User.telegram_id == telegram_id)
        user = (await session.execute(stmt)).scalar_one_or_none()
        return user.language if user and user.language else "he"

@router.message(Command("help"))
async def cmd_help(msg: Message):
    lang = await get_user_lang(msg.from_user.id)
    title = translator.t(lang, "help_title")
    body = f"""
{translator.t(lang, 'savings')}
/start /compare /wallet /why /business /budget /profile /expenses /addexpense /setincome /delexpense

{translator.t(lang, 'household')}
/household /shopping /chore

{translator.t(lang, 'academy')}
/crypto /cbdc /decentral /socio /anti /edu /academy_extended /academy_nft /academy_dao /vision /spark /academia

{translator.t(lang, 'community')}
/ref /qr /stats /top /tip /contact /faq /daily /mydata /gift

{translator.t(lang, 'tools')}
/miniapp /keyboard /hide /ask /feedback /help /quiz /menu

{translator.t(lang, 'permissions')}
/requestadmin /addadmin /login /setpassword /removeadmin

{translator.t(lang, 'admin')}
/admin /export /debug /addgroup /groups /report /setrole

{translator.t(lang, 'profile')}
/myrole /mydata
"""
    await msg.answer(f"{title}\n\n{body}", parse_mode="HTML")
