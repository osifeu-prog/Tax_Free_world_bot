import logging
from loguru import logger as loguru_logger
import sys

# הגדרת loguru
loguru_logger.remove()
loguru_logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>", level="INFO")
loguru_logger.add("logs/bot.log", rotation="10 MB", retention="7 days", level="DEBUG")

# wrapper ל-aiogram
class InterceptHandler(logging.Handler):
    def emit(self, record):
        level = loguru_logger.level(record.levelname).name
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        loguru_logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

def get_logger(name=None):
    if name:
        return loguru_logger.bind(name=name)
    return loguru_logger

# פונקציה ללוגים מותאמים לפקודות
async def log_command(user_id, command, status="handled", duration_ms=0, error=None):
    if error:
        loguru_logger.error(f"📩 {user_id}: {command} | {status} | {duration_ms}ms | error: {error}")
    else:
        loguru_logger.info(f"📩 {user_id}: {command} | {status} | {duration_ms}ms")
