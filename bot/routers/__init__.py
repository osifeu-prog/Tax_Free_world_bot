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

routers = [
    start_router,
    compare_router,
    why_router,
    wallet_router,
    business_router,
    help_router,
    id_router,
    contact_router,
    export_router,
    miniapp_router,
    ref_router,
    stats_router,
]
