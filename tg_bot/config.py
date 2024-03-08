import logging
import os
import sys

from dotenv import load_dotenv
from logging import StreamHandler

load_dotenv()

"""Loggers"""
logging.basicConfig(
    level=os.getenv('LOGGING_LEVEL'),  # переменная LOGGING_LEVEL в .env
    filename='main.log',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)
# Далее подготовлен логер для возможности применения к разным хэндлерам бота.
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler = StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

"""Tokens"""
BOT_TOKEN = os.getenv('BOT_TOKEN')
