from .start import router as start_router
from .why import router as why_router
from .wallet import router as wallet_router
from .business import router as business_router
from .help import router as help_router
from .compare import router as compare_router
from .id import router as id_router
from .contact import router as contact_router
from .export import router as export_router
from .miniapp import router as miniapp_router
from .ref import router as ref_router
from .stats import router as stats_router
from .tip import router as tip_router
from .faq import router as faq_router
from .budget import router as budget_router
from .crypto import router as crypto_router
from .cbdc import router as cbdc_router
from .decentral import router as decentral_router
from .socio import router as socio_router
from .anti import router as anti_router
from .edu import router as edu_router
from .profile import router as profile_router

routers = [
    start_router, compare_router, why_router, wallet_router,
    business_router, help_router, id_router, contact_router,
    export_router, miniapp_router, ref_router, stats_router,
    tip_router, faq_router, budget_router,
    crypto_router, cbdc_router, decentral_router,
    socio_router, anti_router, edu_router,
    profile_router,
]
