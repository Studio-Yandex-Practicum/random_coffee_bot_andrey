import asyncio

from tg_bot.handlers.default import default_router
from tg_bot.loader import bot, dp


async def main():
    try:
        dp.include_router(default_router)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
