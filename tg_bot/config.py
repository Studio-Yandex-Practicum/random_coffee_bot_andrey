import logging

from environs import Env

env = Env()
env.read_env()

ADMIN_ID = env.str('ADMIN_ID')
BOT_TOKEN = env.str('BOT_TOKEN')
LOG_LEVEL = env.str('LOG_LEVEL')

logging.basicConfig(level=LOG_LEVEL)
