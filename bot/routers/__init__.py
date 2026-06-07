from bot.routers.start import router as start_router
from bot.routers.help import router as help_router
from bot.routers.export import router as export_router
# ... (הוסף את כל הראוטרים הנוספים  ראה את רשימת הפקודות)
routers = [start_router, help_router, export_router]
