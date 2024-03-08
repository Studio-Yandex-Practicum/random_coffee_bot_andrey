import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler_di import ContextSchedulerDecorator
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'), parse_mode='HTML')
storage = RedisStorage.from_url('redis://localhost:6379/0')
dp = Dispatcher(storage=storage)
jobstores = {
        'default': RedisJobStore(jobs_key='dispatched_trips_jobs',
                                 run_times_key='dispatched_trips_running',
                                 host='localhost',
                                 db='2',
                                 port=os.getenv('REDIS_PORT'))
    }
scheduler = ContextSchedulerDecorator(
        AsyncIOScheduler(timezone='Europe/Moscow', jobstores=jobstores)
    )
scheduler.ctx.add_instance(bot, declared_class=Bot)
scheduler.start()
