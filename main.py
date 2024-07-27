from aiogram import types
from aiogram.utils import executor
from aiohttp import web

import buttons
from config import dp, bot, Staff
import logging
from handlers import commands, FSM_reg, FSM_store
from db import main_db


async def on_startup(_):
    for i in Staff:
        await bot.send_message(chat_id=i, text='Bot started',
                               reply_markup=buttons.start_buttons)
        # await main_db.sql_create()
async def on_shutdown(_):
    for i in Staff:
        await bot.send_message(chat_id=i, text='Bot stoped')


commands.register_commands(dp)
# quiz.register_quiz(dp)
FSM_reg.register_fsm_for_user(dp)
FSM_store.register_fsm_store(dp)
# notification.register_notification(dp)
# send_products.register_send_products(dp)
# webapp.register_webapp(dp)
#
# admin_group.register_admin_group(dp)

#эхо функция - вызывать самым последним
# echo.register_echo(dp)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
