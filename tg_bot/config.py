import logging

from environs import Env

env = Env()
env.read_env()

ADMIN_ID = env.str('ADMIN_ID')
BOT_TOKEN = env.str('BOT_TOKEN')
DEBUG = env.bool('DEBUG', False)

logging_level = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(level=logging_level)
