from environs import Env

from tg_bot.logs.logs_setup import loggers


env = Env()
env.read_env()

"""Tokens"""
BOT_TOKEN = env.str('BOT_TOKEN')

"""Loggers"""
bot_logger = loggers['BotLogger']

"""Redis"""
redis_host = env.str('REDIS_HOST', None)
redis_port = env.str('REDIS_PORT', None)

"""Django"""
super_user_name = env.str('SUPER_USER_NAME')
super_user_pass = env.str('SUPER_USER_PASS')
