import logging, time
from sqlalchemy import event
from sqlalchemy.engine import Engine

logger = logging.getLogger("db")
logger.setLevel(logging.INFO)

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    context._query_start_time = time.time()
    logger.info(f"➡️ SQL: {statement[:80]}")

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - context._query_start_time
    if total > 0.3:
        logger.warning(f"🐌 SLOW ({total:.3f}s): {statement[:80]}")
