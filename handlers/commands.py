import glob
import random
import os
from aiogram.types import InputFile
from aiogram import types, Dispatcher
from config import bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def start(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Привет! {message.from_user.first_name}\n\n'
                                f'Твой telegram ID - {message.from_user.id}')


async def info(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Бот для пакупки! {message.from_user.first_name}\n\n'
                                f'Твой telegram ID - {message.from_user.id}')


# async def send_mem(call: types.CallbackQuery):
#     path = 'media/'
#     files = glob.glob(os.path.join(path, '*'))
#     random_photo = random.choice(files)
#
#     await bot.send_photo(chat_id=call.from_user.id,
#                          photo=InputFile(random_photo))


def register_commands(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start', 'начало'])
    dp.register_message_handler(info, commands=['info', 'инфо'])
    # dp.register_callback_query_handler(send_mem, text='button_game')