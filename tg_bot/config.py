import os
import logging

from dotenv import load_dotenv

load_dotenv()

"""Logging levels"""
DEBUG = os.getenv('DEBUG')

"""Tokens"""
BOT_TOKEN = os.getenv('BOT_TOKEN')

"""Domain"""
ALLOWED_DOMAIN = os.getenv('ALLOWED_DOMAIN')

logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)

"""Настройки для рассылки"""
MEETING_DAY: str = 'mon'
MEETING_TIME: int = 10
