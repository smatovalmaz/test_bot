from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import buttons

class RegisterUser(StatesGroup):
    productid = State()
    size = State()
    quantity = State()
    phone = State()
    submit = State()

async def fsm_start(message: types.Message):
    await RegisterUser.productid.set()
    await message.answer(text="Введите Артикул:", reply_markup=buttons.cancel)

async def load_productid(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['productid'] = message.text

    await RegisterUser.next()
    await message.answer(text='Введите свой размер:')


async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text

    await RegisterUser.next()
    await message.answer(text='Введите количесто:')


async def load_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['quantity'] = message.text

    await RegisterUser.next()
    await message.answer(text='Введите свой номер телефона:')


async def load_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
#
#     await RegisterUser.next()
#     await message.answer(text='Введите свою почту:')
#
#
# async def load_email(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['email'] = message.text
#
#     await RegisterUser.next()
#     await message.answer(text='Отправьте фото:')
#
#
# async def load_photo(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['photo'] = message.photo[-1].file_id
#
#
#     keyword = InlineKeyboardMarkup(row_width=2)
#     yes_button = InlineKeyboardButton(text='Yes', callback_data='confirm_yes')
#     no_button = InlineKeyboardButton(text='No', callback_data='confirm_no')
#     keyword.add(yes_button,no_button)
#
#     await RegisterUser.next()
#     await message.answer_photo(photo=data['photo'],
#                                caption=f"ФИО - {data['fullname']}\n"
#                                        f"Возраст - {data['age']}\n"
#                                        f"Адрес - {data['adress']}\n"
#                                        f"Номер - {data['phone']}\n"
#                                        f"Почта - {data['email']}\n\n"
#                                        f"<b>Верные данные ?</b>",
#                                reply_markup=keyword, parse_mode=types.ParseMode.HTML)

async def submit (callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'confirm_yes':
        await callback_query.answer('Отлично! Регистрация пройдена', reply_markup=buttons.start_buttons )
        await state.finish()
    elif callback_query.data == 'confirm_no':
        await callback_query.message.answer('Отменено', reply_markup=buttons.start_buttons )
        await state.finish()
    else:
        await callback_query.message.answer(text='Нажмите на кнопку!')


async def cancel_fms(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer(text='Отменено')



def register_fsm_for_user(dp: Dispatcher):
    dp.register_message_handler(cancel_fms,Text(equals='ОТмена',
                                                ignore_case=True), state='*')
    dp.register_message_handler(fsm_start, commands=['registration'])
    dp.register_message_handler(load_productid(), state=RegisterUser.productid)
    dp.register_message_handler(load_size(), state=RegisterUser.size)
    dp.register_message_handler(load_quantity(), state=RegisterUser.quantity)
    # dp.register_message_handler(load_phone, state=RegisterUser.phone)
    # dp.register_message_handler(load_email, state=RegisterUser.email)
    # dp.register_message_handler(load_photo, state=RegisterUser.photo, content_types=['photo'])
    dp.register_callback_query_handler(submit, state=RegisterUser.submit)
