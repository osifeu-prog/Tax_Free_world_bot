import asyncio
import logging
import os
from sqlalchemy import text

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.database.session import engine
from bot.database.models import Base

# ====================== ALL HEALTHY ROUTERS ======================
from bot.routers.academy import router as router_academy
from bot.routers.academy_extended import router as router_academy_extended
from bot.routers.admin import router as router_admin
from bot.routers.admin_groups import router as router_admin_groups
from bot.routers.admin_rbac import router as router_admin_rbac
from bot.routers.admin_requests import router as router_admin_requests
from bot.routers.admin_stats import router as router_admin_stats
from bot.routers.ai_router import router as router_ai_router
from bot.routers.anti import router as router_anti
from bot.routers.ask import router as router_ask
from bot.routers.backup import router as router_backup
from bot.routers.broadcast import router as router_broadcast
from bot.routers.budget import router as router_budget
from bot.routers.business import router as router_business
from bot.routers.categories import router as router_categories
from bot.routers.cbdc import router as router_cbdc
from bot.routers.city import router as router_city
from bot.routers.compare import router as router_compare
from bot.routers.contact import router as router_contact
from bot.routers.course_progress import router as router_course_progress
from bot.routers.crypto import router as router_crypto
from bot.routers.daily import router as router_daily
from bot.routers.dashboard_simple import router as router_dashboard_simple
from bot.routers.db_test import router as router_db_test
from bot.routers.dbstats import router as router_dbstats
from bot.routers.debug import router as router_debug
from bot.routers.decentral import router as router_decentral
from bot.routers.donate import router as router_donate
from bot.routers.edu import router as router_edu
from bot.routers.export import router as router_export
from bot.routers.family_finance import router as router_family_finance
from bot.routers.familygroup import router as router_familygroup
from bot.routers.faq import router as router_faq
from bot.routers.feedback import router as router_feedback
from bot.routers.fix_users import router as router_fix_users
from bot.routers.gamification import router as router_gamification
from bot.routers.generator_handler import router as router_generator_handler
from bot.routers.gift import router as router_gift
from bot.routers.health import router as router_health
from bot.routers.help import router as router_help
from bot.routers.household import router as router_household
from bot.routers.id import router as router_id
from bot.routers.import_users import router as router_import_users
from bot.routers.incomes import router as router_incomes
from bot.routers.init_donations import router as router_init_donations
from bot.routers.init_events import router as router_init_events
from bot.routers.init_indexes import router as router_init_indexes
from bot.routers.init_useless_log import router as router_init_useless_log
from bot.routers.keyboard import router as router_keyboard
from bot.routers.language import router as router_language
from bot.routers.loadplan import router as router_loadplan
from bot.routers.market import router as router_market
from bot.routers.menu import router as router_menu
from bot.routers.miniapp import router as router_miniapp
from bot.routers.morning import router as router_morning
from bot.routers.mydata import router as router_mydata
from bot.routers.ocr import router as router_ocr
from bot.routers.pension import router as router_pension
from bot.routers.profile import router as router_profile
from bot.routers.profile_citizen import router as router_profile_citizen
from bot.routers.qr import router as router_qr
from bot.routers.quiz import router as router_quiz
from bot.routers.receipt import router as router_receipt
from bot.routers.ref import router as router_ref
from bot.routers.report import router as router_report
from bot.routers.report_pension import router as router_report_pension
from bot.routers.request_admin import router as router_request_admin
from bot.routers.saveplan import router as router_saveplan
from bot.routers.seed_courses import router as router_seed_courses
from bot.routers.seed_kg import router as router_seed_kg
from bot.routers.setwallet import router as router_setwallet
from bot.routers.socio import router as router_socio
from bot.routers.start import router as router_start
from bot.routers.stats import router as router_stats
from bot.routers.stats_useless import router as router_stats_useless
from bot.routers.tip import router as router_tip
from bot.routers.useless import router as router_useless
from bot.routers.wallet import router as router_wallet
from bot.routers.webapp import router as router_webapp
from bot.routers.welcome_onboarding import router as router_welcome_onboarding
from bot.routers.why import router as router_why

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    
    # Include all routers
    dp.include_router(router_academy)
    dp.include_router(router_academy_extended)
    dp.include_router(router_admin)
    dp.include_router(router_admin_groups)
    dp.include_router(router_admin_rbac)
    dp.include_router(router_admin_requests)
    dp.include_router(router_admin_stats)
    dp.include_router(router_ai_router)
    dp.include_router(router_anti)
    dp.include_router(router_ask)
    dp.include_router(router_backup)
    dp.include_router(router_broadcast)
    dp.include_router(router_budget)
    dp.include_router(router_business)
    dp.include_router(router_categories)
    dp.include_router(router_cbdc)
    dp.include_router(router_city)
    dp.include_router(router_compare)
    dp.include_router(router_contact)
    dp.include_router(router_course_progress)
    dp.include_router(router_crypto)
    dp.include_router(router_daily)
    dp.include_router(router_dashboard_simple)
    dp.include_router(router_db_test)
    dp.include_router(router_dbstats)
    dp.include_router(router_debug)
    dp.include_router(router_decentral)
    dp.include_router(router_donate)
    dp.include_router(router_edu)
    dp.include_router(router_export)
    dp.include_router(router_family_finance)
    dp.include_router(router_familygroup)
    dp.include_router(router_faq)
    dp.include_router(router_feedback)
    dp.include_router(router_fix_users)
    dp.include_router(router_gamification)
    dp.include_router(router_generator_handler)
    dp.include_router(router_gift)
    dp.include_router(router_health)
    dp.include_router(router_help)
    dp.include_router(router_household)
    dp.include_router(router_id)
    dp.include_router(router_import_users)
    dp.include_router(router_incomes)
    dp.include_router(router_init_donations)
    dp.include_router(router_init_events)
    dp.include_router(router_init_indexes)
    dp.include_router(router_init_useless_log)
    dp.include_router(router_keyboard)
    dp.include_router(router_language)
    dp.include_router(router_loadplan)
    dp.include_router(router_market)
    dp.include_router(router_menu)
    dp.include_router(router_miniapp)
    dp.include_router(router_morning)
    dp.include_router(router_mydata)
    dp.include_router(router_ocr)
    dp.include_router(router_pension)
    dp.include_router(router_profile)
    dp.include_router(router_profile_citizen)
    dp.include_router(router_qr)
    dp.include_router(router_quiz)
    dp.include_router(router_receipt)
    dp.include_router(router_ref)
    dp.include_router(router_report)
    dp.include_router(router_report_pension)
    dp.include_router(router_request_admin)
    dp.include_router(router_saveplan)
    dp.include_router(router_seed_courses)
    dp.include_router(router_seed_kg)
    dp.include_router(router_setwallet)
    dp.include_router(router_socio)
    dp.include_router(router_start)
    dp.include_router(router_stats)
    dp.include_router(router_stats_useless)
    dp.include_router(router_tip)
    dp.include_router(router_useless)
    dp.include_router(router_wallet)
    dp.include_router(router_webapp)
    dp.include_router(router_welcome_onboarding)
    dp.include_router(router_why)
    
    logger.info("🚀 Bot starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


