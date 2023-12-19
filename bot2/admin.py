from aiogram.utils.exceptions import MessageNotModified
from main import bot, dp
from aiogram.types import Message, InputMediaPhoto
from aiogram import types, Dispatcher
from config import admins, BotConfig, merchant_id, api_key
import markups as nav
from utils.db import DataBase
import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, KeyboardButton, \
    ReplyKeyboardMarkup
from utils.api import Api
import datetime
import time
from kassa import get_balance

api = Api()

db = DataBase('db.db')

bot_config = BotConfig()
bot_config.load_from_database()

class addChannels(StatesGroup):
    name = State()
    id = State()
    url = State()

class AddTime(StatesGroup):
    id = State()
    time = State()


@dp.message_handler(commands=['admin'])
async def send(message: Message):
    if message.chat.type == 'private':
        if message.from_user.id in admins:
            stats = db.stats_users()
            balance = api.balance()
            post = db.get_count_post()
            rent = db.get_count_rent()
            nonce = str(int(time.time()))
            fk_balance = get_balance(merchant_id, nonce, api_key)
            await bot.send_message(message.from_user.id, '<b>Админ-панель:</b>\n\nПользователей в боте: <b>{0}</b>\nБаланс на площадке: <b>{1}$</b>\nБаланс Free-Kassa: {2}₽\nВсего добавлено постов: <b>{3}</b>\nВсего куплено аренд: <b>{4}</b>'.format(stats[0], round(float(balance['balance']), 2), fk_balance, post, rent), reply_markup=nav.adminsMenu, parse_mode='HTML')

@dp.callback_query_handler(text_contains='admin_', state=None)
async def subchannelDone(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data == 'admin_2':
        post_message, keyboard = nav.generate_postmenuAdm()
        await bot.send_message(call.from_user.id, text=post_message, reply_markup=keyboard, parse_mode="HTML", disable_web_page_preview=True)
    if call.data == 'admin_3':
        await AddTime.id.set()
        await bot.send_message(call.from_user.id, 'Для выдачи аредного времени пришлите id пользователя:')
    if call.data == 'admin_4':
        await bot.send_message(call.from_user.id, '📖 Выберите что хотите сделать:', reply_markup=nav.channelsMenu)
    if call.data == 'admin_5':
        await bot.send_message(call.from_user.id, '📖 Выберите что хотите отредактировать:', reply_markup=nav.configMenu)

@dp.callback_query_handler(text_contains='config', state=None)
async def geolocat(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data == 'config_1':
        await bot.send_message(call.from_user.id, f'Текущеее значение - {bot_config.param1} - Укажите новое значение.')
        db.setState(101, call.from_user.id)
    if call.data == 'config_2':
        await bot.send_message(call.from_user.id, f'Текущеее значение - {bot_config.param2} - Укажите новое значение.')
        db.setState(102, call.from_user.id)
    if call.data == 'config_3':
        await bot.send_message(call.from_user.id, f'Текущеее значение - {bot_config.param3} - Укажите новое значение.')
        db.setState(103, call.from_user.id)
    if call.data == 'config_4':
        await bot.send_message(call.from_user.id, f'Текущеее значение - {bot_config.param4} - Укажите новое значение.')
        db.setState(104, call.from_user.id)
    if call.data == 'config_5':
        await bot.send_message(call.from_user.id, f'Текущеее значение - {bot_config.param5} - Укажите новое значение.')
        db.setState(105, call.from_user.id)
    if call.data == 'config_6':
        await bot.send_message(call.from_user.id, f'Текущеее значение - {bot_config.param6} - Укажите новое значение.')
        db.setState(106, call.from_user.id)
    if call.data == 'config_7':
        await bot.send_message(call.from_user.id, f'Текущеее значение - {bot_config.param7} - Укажите новое значение.')
        db.setState(107, call.from_user.id)
    if call.data == 'config_8':
        await bot.send_message(call.from_user.id, f'Текущеее значение - {bot_config.param8} - Укажите новое значение.')
        db.setState(108, call.from_user.id)
    if call.data == 'config_9':
        await bot.send_message(call.from_user.id, f'Текущеее значение - {bot_config.param9} - Укажите новое значение.')
        db.setState(109, call.from_user.id)

@dp.callback_query_handler(lambda call: call.data.startswith('next_page') or call.data.startswith('prev_page'))
async def handle_page_transition(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    page_data = call.data.split(':')
    page_direction = page_data[0]
    target_page = int(page_data[1])
    if page_direction == 'next_page':
        post_message, keyboard = nav.generate_postmenuAdm(page=target_page)

        await bot.send_message(call.from_user.id, post_message, reply_markup=keyboard, parse_mode="HTML",  disable_web_page_preview=True)
    elif page_direction == 'prev_page':
        post_message, keyboard = nav.generate_postmenuAdm(page=target_page)
        await bot.send_message(call.from_user.id, post_message, reply_markup=keyboard, parse_mode="HTML",  disable_web_page_preview=True)
    else:
        pass

@dp.callback_query_handler(text_contains='channels', state=None)
async def geolocat(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.from_user.id in admins and call.data == 'channels_1':
        await addChannels.name.set()
        await bot.send_message(call.from_user.id, '🚀 Напишите название канала которое будет отображаться:')
    if call.from_user.id in admins and call.data == 'channels_2':
        channels = db.channels_get()
        text = []
        for channel in channels:
            text.append("<b>" + channel[2] + "</b> - " + channel[3])
        await bot.send_message(call.from_user.id, '🗓 <b>Список каналов:</b>\n\n' + "\n".join(text), reply_markup=nav.showChannelsAdm(), disable_web_page_preview=True, parse_mode="HTML")

@dp.callback_query_handler(text_contains='delete', state=None)
async def geolocat(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.from_user.id in admins and call.data.split("_")[0] == 'delete':
        id_channel = call.data.split("_")[1]
        db.channel_delete(id_channel)
        await bot.send_message(call.from_user.id, '✅ Успешных удалено!')

@dp.message_handler(state=AddTime.id)
async def load_name(message: types.Message, state: FSMContext):
    id = message.text
    await state.update_data({'id': id})
    await AddTime.next()
    await message.reply('Теперь укажите время выдачи арендного периода в часах: ')

@dp.message_handler(state=AddTime.time)
async def load_user_id(message: types.Message, state: FSMContext):
    time = message.text
    id = await state.get_data('id')
    id = id.get('id')
    future_time = float(time) * 60 * 60
    rental_time = datetime.datetime.now().timestamp() + future_time
    await state.finish()
    db.update_rental(rental_time, id)
    await bot.send_message(message.from_user.id, '✅ Аренда была успешно выдана!')

@dp.message_handler(state=addChannels.name)
async def load_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data({'name': name})
    await addChannels.next()
    await message.reply('🤔 Теперь введите id канала: ')

@dp.message_handler(state=addChannels.id)
async def load_user_id(message: types.Message, state: FSMContext):
    id = message.text
    await state.update_data({'id': id})
    await addChannels.next()
    await message.reply('👀 Теперь введите url этого канала: ')

@dp.message_handler(state=addChannels.url)
async def load_user_id(message: types.Message, state: FSMContext):
    url = message.text
    await state.update_data({'url': url})
    name = await state.get_data('name')
    name = name.get('name')
    id = await state.get_data('id')
    id = id.get('id')
    url = await state.get_data('url')
    url = url.get('url')
    db.channels_save(id, name, url)
    await state.finish()
    await bot.send_message(message.from_user.id, '✅ Все данные были успешно сохранены')

    

