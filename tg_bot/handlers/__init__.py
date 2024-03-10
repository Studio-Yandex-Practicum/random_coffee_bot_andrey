from tg_bot.handlers.default import default_router
from tg_bot.handlers.admin import admin_router

all_routers = (
    default_router,
    admin_router,
)
