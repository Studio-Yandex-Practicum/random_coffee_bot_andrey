from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler_di import ContextSchedulerDecorator
from tg_bot.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
storage = RedisStorage.from_url('redis://localhost:6379/0')
dp = Dispatcher(storage=storage)
jobstores = {
    'default': RedisJobStore(jobs_key='dispatched_trips_jobs',
                             run_times_key='dispatched_trips_running',
                             host='localhost',
                             db='2',
                             port=6379)
}
sheduler = ContextSchedulerDecorator(
    AsyncIOScheduler(timezone='Europe/Moscow', jobstores=jobstores)
)
sheduler.ctx.add_instance(bot, declared_class=Bot)

sheduler.start()
