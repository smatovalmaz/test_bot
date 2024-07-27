from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           KeyboardButton, ReplyKeyboardMarkup)
import buttons
# from db import main_db


class store(StatesGroup):
    name_product = State()
    size = State()
    price = State()
    productid = State()
    category = State()
    infoproduct = State()
    photo = State()
    submit = State()


async def fsm_start(message: types.Message):
    await store.name_product.set()
    await message.answer(text="Введите название товара:", reply_markup=buttons.cancel)


async def load_name_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_product'] = message.text

    await store.next()
    await message.answer(text='Введите размер одежды')


async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text

    await store.next()
    await message.answer(text='Введите цену товара: ')


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    await store.next()
    await message.answer(text='Введите артикул: ')


async def load_productid(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['productid'] = message.text

    await store.next()
    await message.answer('Напишите категорию товара:')

async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text

    await store.next()
    await message.answer('Напишите категорию товара:')

async def load_infoproduct(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
            data['infoproduct'] = message.text


    await store.next()
    kb = types.ReplyKeyboardRemove()
    await message.answer(text='Отправьте фотку товара:', reply_markup=kb)


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

    keyboard = ReplyKeyboardMarkup(row_width=2)
    keyboard.add(KeyboardButton('Да'), KeyboardButton('Нет'))

    await store.next()
    await message.answer_photo(photo=data['photo'],
                               caption=f"Название - {data['name_product']}\n"
                                       f"Размер - {data['size']}\n"
                                       f"Цена - {data['price']}\n"
                                       f"Артикул - {data['productid']}\n\n"
                                       f"<b>Верные ли данные ?</b>",
                               reply_markup=keyboard, parse_mode=types.ParseMode.HTML)


async def submit(message: types.Message, state: FSMContext):
    if message.text == 'Да':
        async with state.proxy() as data:
            await main_db.sql_insert_store(
                name_product=data['name_product'],
                size=data['size'],
                price=data['price'],
                productid=data['productid'],
                photo=data['photo']
            )
            await message.answer('Отлично! Регистрация пройдена.', reply_markup=buttons.start_buttons)
            await state.finish()
    elif message.text == 'Нет':
        await message.answer('Отменено!', reply_markup=buttons.start_buttons)
        await state.finish()

    else:
        await message.answer(text='Нажмите на кнопку!')


async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer(text='Отменено')


# Finite State Machine
def register_fsm_store(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='Отмена',
                                                 ignore_case=True), state='*')
    dp.register_message_handler(fsm_start, commands=['store'])
    dp.register_message_handler(load_name_product, state=store.name_product)
    dp.register_message_handler(load_size, state=store.size)
    dp.register_message_handler(load_price, state=store.price)
    dp.register_message_handler(load_productid, state=store.productid)
    dp.register_message_handler(load_category, state=store.category)
    dp.register_message_handler(load_infoproduct, state=store.infoproduct)
    dp.register_message_handler(load_photo, state=store.photo, content_types=['photo'])
    dp.register_message_handler(submit, state=store.submit)