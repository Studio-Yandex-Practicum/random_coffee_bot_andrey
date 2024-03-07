import os
import logging

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=os.getenv('DEBUG'))

"""Tokens"""
BOT_TOKEN = os.getenv('BOT_TOKEN')
