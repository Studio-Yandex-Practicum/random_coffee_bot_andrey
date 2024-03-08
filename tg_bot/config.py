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


# env = Env()
# env.read_env()

"""Tokens"""
# BOT_TOKEN = env.str('BOT_TOKEN')

"""Loggers"""
# bot_logger = loggers['BotLogger']

"""Redis"""
# redis_host = env.str('REDIS_HOST', None)
# redis_port = env.str('REDIS_PORT', None)

"""Django"""
# super_user_name = env.str('SUPER_USER_NAME')
# super_user_pass = env.str('SUPER_USER_PASS')
