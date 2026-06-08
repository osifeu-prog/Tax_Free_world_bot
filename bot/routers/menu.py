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

@router.message(Command("menu"))
async def cmd_menu(msg: Message):
    lang = await get_user_lang(msg.from_user.id)
    text = f"""
<b>{translator.t(lang, 'menu_title')}</b>
━━━━━━━━━━━━━━━━━━━━━━
{translator.t(lang, 'savings')}
/start /compare /wallet /why /business /budget /profile /expenses /addexpense /setincome /delexpense
{translator.t(lang, 'household')}
/household /shopping /chore /familygroup
{translator.t(lang, 'academy')}
/academy /crypto /cbdc /decentral /socio /anti /edu /academy_extended /academy_nft /academy_dao /vision /spark
{translator.t(lang, 'community')}
/ref /qr /stats /top /tip /contact /faq /daily /mydata /gift
{translator.t(lang, 'tools')}
/miniapp /keyboard /hide /ask /feedback /help /quiz /menu /language
{translator.t(lang, 'permissions')}
/requestadmin /addadmin /login /setpassword /removeadmin
{translator.t(lang, 'admin')}
/admin /export /debug /addgroup /groups /report /setrole /seed_courses
{translator.t(lang, 'profile')}
/myrole /mydata /setwallet
📊 <b>פנסיה</b>
/pension
💖 <b>תרומה</b>
/donate
"""
    await msg.answer(text, parse_mode="HTML")
