from aiogram.utils.exceptions import MessageNotModified
from main import bot, dp
from aiogram.types import Message, InputMediaPhoto
from aiogram import types, Dispatcher
from config import admins
import markups as nav
from db import DataBase
import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, KeyboardButton, \
    ReplyKeyboardMarkup

db = DataBase('db.db')

class ConfigBon(StatesGroup):
    editConfig = State()

class ConfigMin(StatesGroup):
    editConfig = State()

class addUrl(StatesGroup):
    url = State()

class addChannels(StatesGroup):
    name = State()
    id = State()
    url = State()

class addCC(StatesGroup):
    photo = State()
    name = State()
    description = State()
    url = State()


@dp.message_handler(commands=['admin'])
async def send(message: Message):
    if message.chat.type == 'private':
        if message.from_user.id in admins:
            stats = db.stats_users()
            vipl = db.get_vipl()
            await bot.send_message(message.from_user.id, '<b>Админ-панель:</b>\n\nПользователей в боте: <b>{0}</b>\nВыплачено всего: <b>{1}₽</b>'.format(stats[0], vipl[0]), reply_markup=nav.adminsMenu, parse_mode='HTML')

@dp.callback_query_handler(text_contains='admin_', state=None)
async def subchannelDone(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data == 'admin_2':
        await bot.send_message(call.from_user.id, '📖 Выберите что хотите сделать:', reply_markup=nav.channelsMenu)
    if call.data == 'admin_3':
        await bot.send_message(call.from_user.id, '📎 Выберите что хотите сделать:', reply_markup=nav.CCMenu)
    if call.data == 'admin_4':
        await bot.send_message(call.from_user.id, 'Введите новый url ссылки "Заработка обучения":')
        await addUrl.url.set()
    if call.data == 'admin_5':
        await bot.send_message(call.from_user.id, '⚙️ Выберите что хотите сделать:', reply_markup=nav.configMenu)
    if call.data == 'admin_6':
        outputs = db.get_output()
        if (outputs != ""):
            for output in outputs:
                outputMenu = InlineKeyboardMarkup(row_width=2)
                accept = InlineKeyboardButton(text="✅ Принять", callback_data="accept_" + str(output[0]))
                returs = InlineKeyboardButton(text="❌ Отклонить", callback_data="returs_" + str(output[0]))
                outputMenu.insert(accept)
                outputMenu.insert(returs)
                await bot.send_message(call.from_user.id, '📤 Заявка <a href="tg://user?id={0}">пользователя:</a>\n\n▫️ ID: {0}\n▫️ Кошелёк: {1}\n▫️ Сумма: {2}'.format(output[1], output[3], output[2]), reply_markup=outputMenu)
        if not db.get_output():
            await bot.send_message(call.from_user.id, '❌ Заявок на выплату нет')

@dp.callback_query_handler(text_contains='accept_', state=None)
async def subchannelDone(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data.split("_")[0] == 'accept':
        id = call.data.split("_")[1]
        db.accept_vipl(id)
        user_id = db.get_accept(id)[0]
        await bot.send_message(call.from_user.id, '✅ Успешно выплачено')
        await bot.send_message(user_id, '✅ Ваша заявка на выплату была успешно исполнена!')

@dp.callback_query_handler(text_contains='returs_', state=None)
async def subchannelDone(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data.split("_")[0] == 'returs':
        id = call.data.split("_")[1]
        user_id = db.get_accept(id)[0]
        await bot.send_message(call.from_user.id, '❌ Заявка на вывод была отменена!')
        await bot.send_message(user_id, '❌ Ваша заявка на вывод была отменена!')
        db.delete_vipl(id)


@dp.callback_query_handler(text_contains='config_', state=None)
async def subchannelDone(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data == 'config_1':
        await bot.send_message(call.from_user.id, 'Введите новое значение для реферального бонуса: ')
        await ConfigBon.editConfig.set()
    if call.data == 'config_2':
        await bot.send_message(call.from_user.id, 'Введите новое значение для размера минимальной суммы на выплату: ')
        await ConfigMin.editConfig.set()

@dp.message_handler(state=ConfigBon.editConfig)
async def load_user_id(message: types.Message, state: FSMContext):
    editConfig = message.text
    db.edit_config(editConfig)
    await state.finish()
    await bot.send_message(message.from_user.id, '✅ Все данные были успешно сохранены')

@dp.message_handler(state=ConfigMin.editConfig)
async def load_user_id(message: types.Message, state: FSMContext):
    editConfig = message.text
    db.edit_configMin(editConfig)
    await state.finish()
    await bot.send_message(message.from_user.id, '✅ Все данные были успешно сохранены')

@dp.message_handler(state=addUrl.url)
async def load_user_id(message: types.Message, state: FSMContext):
    url = message.text
    db.edit_url(url)
    await state.finish()
    await bot.send_message(message.from_user.id, '✅ Все данные были успешно сохранены')

@dp.callback_query_handler(text_contains='channels', state=None)
async def geolocat(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.from_user.id in admins and call.data == 'channelsAdd':
        await addChannels.name.set()
        await bot.send_message(call.from_user.id, '🚀 Напишите название канала которое будет отображаться:')
    if call.from_user.id in admins and call.data == 'channelsMin':
        channels = db.channels_get()
        text = []
        for channel in channels:
            text.append("<b>" + channel[0] + "</b> - " + channel[2])
        await bot.send_message(call.from_user.id, '🗓 <b>Список каналов:</b>\n\n' + "\n".join(text), reply_markup=nav.showChannelsAdm(), disable_web_page_preview=True)

@dp.callback_query_handler(text_contains='delete', state=None)
async def geolocat(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.from_user.id in admins and call.data.split("_")[0] == 'delete':
        id_channel = call.data.split("_")[1]
        db.channel_delete(id_channel)
        await bot.send_message(call.from_user.id, '✅ Успешных удалено!')

@dp.callback_query_handler(text_contains='backAdm', state=None)
async def geolocat(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.from_user.id in admins and call.data == 'backAdm':
        stats = db.stats_users()
        await bot.send_message(call.from_user.id, '<b>Админ-панель:</b>\n\nПользователей в боте: <b>{0}</b>'.format(stats[0]), reply_markup=nav.adminsMenu, parse_mode='HTML')

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
    db.channels_save(name, id, url)
    await state.finish()
    await bot.send_message(message.from_user.id, '✅ Все данные были успешно сохранены')

@dp.callback_query_handler(text_contains='CC', state=None)
async def geolocat(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.from_user.id in admins and call.data == 'CCAdd':
        await addCC.photo.set()
        await bot.send_message(call.from_user.id, '🔴 Для начала загрузите фото')
    if call.from_user.id in admins and call.data == 'CCMin':
        ccs = db.cc_get()
        text = []
        for cc in ccs:
            text.append("<b>" + cc[2] + "</b> - " + cc[4])
        await bot.send_message(call.from_user.id, '🗓 <b>Список казино:</b>\n\n' + "\n".join(text), reply_markup=nav.showCCAdm(), disable_web_page_preview=True)

@dp.callback_query_handler(text_contains='stop', state=None)
async def geolocat(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.from_user.id in admins and call.data.split("_")[0] == 'stop':
        id = call.data.split("_")[1]
        db.cc_delete(id)
        await bot.send_message(call.from_user.id, '✅ Успешных удалено!')

@dp.message_handler(content_types=['photo'], state=addCC.photo)
async def load_photo(message: types.Message, state:FSMContext):
    photo = message.photo[0].file_id
    await state.update_data({'photo': photo})
    await addCC.next()
    await message.reply('🟠 Введите заголовок который будет отображаться')

@dp.message_handler(state=addCC.name)
async def load_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data({'name': name})
    await addCC.next()
    await message.reply('🤔 Теперь введите описание:')

@dp.message_handler(state=addCC.description)
async def load_name(message: types.Message, state: FSMContext):
    description = message.text
    await state.update_data({'description': description})
    await addCC.next()
    await message.reply('🤔 Теперь введите url потока:')

@dp.message_handler(state=addCC.url)
async def load_user_id(message: types.Message, state: FSMContext):
    url = message.text
    await state.update_data({'url': url})
    photo = await state.get_data('photo')
    photo = photo.get('photo')
    name = await state.get_data('name')
    name = name.get('name')
    description = await state.get_data('description')
    description = description.get('description')
    url = await state.get_data('url')
    url = url.get('url')
    db.cc_save(photo, name, description, url)
    await state.finish()
    await bot.send_message(message.from_user.id, '✅ Все данные были успешно сохранены')

def updateConfig():
    REF_BONUS = db.get_refBonus()[0]
    return REF_BONUS

def updateConfigOne():
    Min_payOut = db.get_MinpayOUt()[0]
    return Min_payOut
