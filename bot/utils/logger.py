# -*- coding: utf-8 -*-
import logging, sys

def setup_logger():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", stream=sys.stdout)
    return logging.getLogger("bot")

logger = setup_logger()

