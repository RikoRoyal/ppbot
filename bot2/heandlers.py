import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import hashlib
from http.client import responses
import logging
import os
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, KeyboardButton, \
    ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified
from main import bot, dp
from aiogram.types import Message, InputMediaPhoto, InputTextMessageContent, InlineQueryResultArticle, ChatActions
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import ContentTypeFilter, ForwardedMessageFilter
import datetime
from config import admins, not_sub_message, BOT_NICKNAME, BotConfig
import markups as nav
from utils.db import DataBase
import admin, mail
from utils.api import Api


db = DataBase('db.db')

api = Api()

bot_config = BotConfig()
bot_config.load_from_database()

services = api.services()  # Return all services

class addPost(StatesGroup):
    url = State()
    amount = State()

async def send_to_admin(dp):
    try:
        i = 0
        for i in range(len(admins)):
            await bot.send_message(chat_id=admins[i], text='✅ Бот запущен')
    except Exception as e:
        pass

async def check_sub_channels(channels, user_id):
    for channel in channels:
        chat_member = await bot.get_chat_member(chat_id=channel[1], user_id=user_id)
        if chat_member['status'] == 'left':
            return False
    return True

async def checkdays():
    d = datetime.datetime.now()
    date = d.timestamp()
    bm = db.check_date(date)
    for b in bm:
        await update_entry(b)

async def update_entry(entry):
        db.update_entry(entry[1])
        await bot.send_message(entry[1], "Срок вашей аренды истек!", reply_markup=nav.greet_kb)

async def checkviews():
    order_ids = db.get_orderAll()
    for order_id in order_ids:
        remains = api.status(order_id)['remains']
        if remains == '0':
            db.delete_post(order_id[0])

@dp.message_handler(commands=['start'])
async def starting(message: Message):
    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            start_command = message.text
            referer_id = str(start_command[7:])
            if str(referer_id) != "":
                if str(referer_id) != str(message.from_user.id):
                    db.add_user(message.from_user.id, referer_id)
                    await bot.send_message(message.from_user.id, "👨🏻‍💻 Привет!\n\nБот позволяет накручивать просмотры на посты открытых каналов Telegram.\n\nЖми 📆 Тестовый период для начала работы и ознакомления с функционалом бота.\n\n🤚Чтобы продолжить, вам нужно всего лишь подписаться на каналы спонсоров👇🏻✨", reply_markup=nav.showChannels(message.from_user.id))
                    await bot.send_message(referer_id, "🎁 У вас новый реферал!")
                else:
                    db.add_user(message.from_user.id)
                    await bot.send_message(message.from_user.id, "👨🏻‍💻 Привет!\n\nБот позволяет накручивать просмотры на посты открытых каналов Telegram.\n\nЖми 📆 Тестовый период для начала работы и ознакомления с функционалом бота.\n\n🤚Чтобы продолжить, вам нужно всего лишь подписаться на каналы спонсоров👇🏻✨", reply_markup=nav.showChannels(message.from_user.id))
            else:
                db.add_user(message.from_user.id)
                await bot.send_message(message.from_user.id, "👨🏻‍💻 Привет!\n\nБот позволяет накручивать просмотры на посты открытых каналов Telegram.\n\nЖми 📆 Тестовый период для начала работы и ознакомления с функционалом бота.\n\n🤚Чтобы продолжить, вам нужно всего лишь подписаться на каналы спонсоров👇🏻✨", reply_markup=nav.showChannels(message.from_user.id))
        else:
            status = db.check_status(message.from_user.id)[0]
            if status == 1:
                await bot.send_message(message.from_user.id, "👨🏻‍💻 Привет!\n\nБот позволяет накручивать просмотры на посты открытых каналов Telegram.\n\nЖми 📆 Тестовый период для начала работы и ознакомления с функционалом бота.", reply_markup=nav.rental_kb)
            else:
                channels = db.channels_get()
                if not await check_sub_channels(channels, message.from_user.id) or channels is None:
                    await bot.send_message(message.from_user.id, "👨🏻‍💻 Привет!\n\nБот позволяет накручивать просмотры на посты открытых каналов Telegram.\n\nЖми 📆 Тестовый период для начала работы и ознакомления с функционалом бота.\n\n🤚Чтобы продолжить, вам нужно всего лишь подписаться на каналы спонсоров👇🏻✨", reply_markup=nav.showChannels(message.from_user.id))
                else:
                    await bot.send_message(message.from_user.id, "👨🏻‍💻 Привет!\n\nБот позволяет накручивать просмотры на посты открытых каналов Telegram.\n\nЖми 📆 Тестовый период для начала работы и ознакомления с функционалом бота.", reply_markup=nav.greet_kb)

@dp.callback_query_handler(text_contains='subchannelDone')
async def subchannelDone(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    channels = db.channels_get()
    if await check_sub_channels(channels, call.from_user.id):
        await bot.send_message(call.from_user.id, "Спасибо за подписку! Теперь вы можете пользоваться нашими услугами.", reply_markup=nav.greet_kb)
    else:
        await call.answer(text=not_sub_message, show_alert=True)
        await bot.send_message(call.from_user.id, '📝 <b>Для использования бота, вы должны быть подписаны на наши каналы:</b>', reply_markup=nav.showChannels(call.from_user.id), parse_mode="HTML")
        
@dp.message_handler(state=addPost, text='⏹ Отмена')
async def cancel_button_handler_inside_state(message: types.Message, state: FSMContext):
    await state.reset_state() 
    await message.answer("Добавление поста было отменено.", reply_markup=nav.rental_kb)

@dp.message_handler(content_types=['text'], state=None)
async def text_menu(message: Message):
    state = db.getState(message.from_user.id)[0]
    value = message.text
    if state != 0:
        if value.isdigit():
            if state == 101:
                db.updateConfig('max_post', value)
                await bot.send_message(message.from_user.id, 'Данные были успешно обновлены!')
                bot_config.load_from_database()
                db.setState(0, message.from_user.id)
            if state == 102:
                db.updateConfig('limit_post', value)
                await bot.send_message(message.from_user.id, 'Данные были успешно обновлены!')
                bot_config.load_from_database()
                db.setState(0, message.from_user.id)
            if state == 103:
                db.updateConfig('price_1', value)
                await bot.send_message(message.from_user.id, 'Данные были успешно обновлены!')
                bot_config.load_from_database()
                db.setState(0, message.from_user.id)
            if state == 104:
                db.updateConfig('price_2', value)
                await bot.send_message(message.from_user.id, 'Данные были успешно обновлены!')
                bot_config.load_from_database()
                db.setState(0, message.from_user.id)
            if state == 105:
                db.updateConfig('price_3', value)
                await bot.send_message(message.from_user.id, 'Данные были успешно обновлены!')
                bot_config.load_from_database()
                db.setState(0, message.from_user.id)
            if state == 106:
                db.updateConfig('price_4', value)
                await bot.send_message(message.from_user.id, 'Данные были успешно обновлены!')
                bot_config.load_from_database()
                db.setState(0, message.from_user.id)
            if state == 107:
                db.updateConfig('price_5', value)
                await bot.send_message(message.from_user.id, 'Данные были успешно обновлены!')
                bot_config.load_from_database()
                db.setState(0, message.from_user.id)
            if state == 108:
                db.updateConfig('price_6', value)
                await bot.send_message(message.from_user.id, 'Данные были успешно обновлены!')
                bot_config.load_from_database()
                db.setState(0, message.from_user.id)
            if state == 109:
                db.updateConfig('price_7', value)
                await bot.send_message(message.from_user.id, 'Данные были успешно обновлены!')
                bot_config.load_from_database()
                db.setState(0, message.from_user.id)
        else:
            await bot.send_message(message.from_user.id, 'Вы прислали что-то не внятное')
            db.setState(0, message.from_user.id)
    if message.chat.type == 'private':
        if message.text == '👥 Рефералы':
            number_referrals = db.count_referes(message.from_user.id)[0]
            await bot.send_message(message.from_user.id, '<b>👥 Партнёрская программа 👥</b>\n\n👤 Ваши приглашённые: <b>{0}</b>\n\n🔗 Ваша партнёрская ссылка: https://t.me/{1}?start={2}\n\n🤝 Приглашайте <b>друзей</b> и получайте наше уважение!.'.format(number_referrals, BOT_NICKNAME, message.from_user.id), parse_mode="HTML", disable_web_page_preview=True)
        if message.text == '💷 Арендовать бота':
            await bot.send_message(message.from_user.id, f'💶 Для полноценного использования бота необходимо оплатить аренду.\n\nСтоимость аренды:\n1 день - {bot_config.param3}₽\n3 дня - {bot_config.param4}₽\n7 дней - {bot_config.param5}₽\n1 месяц - {bot_config.param6}₽\n3 месяца - {bot_config.param7}₽\n6 месяцев - {bot_config.param8}₽\n12 месяцев - {bot_config.param9}₽', reply_markup=nav.generate_payment_buttons(message.from_user.id))
        if message.text == '💷 Управление арендой':
            time = db.date_rental(message.from_user.id)[0]
            if time is not None:
                current_time = datetime.datetime.now().timestamp()
                time_diff = time - current_time
                days = int(time_diff // (3600 * 24))
                hours = int((time_diff % (3600 * 24)) // 3600)
                minutes = int((time_diff % 3600) // 60)
                seconds = int(time_diff % 60)
                await bot.send_message(message.from_user.id, f'🕐 Осталось {days}д {hours}ч {minutes}мин {seconds}сек\n\nСтоимость продления аренды:\n1 день - {bot_config.param3}₽\n3 дня - {bot_config.param4}₽\n7 дней - {bot_config.param5}₽\n1 месяц - {bot_config.param6}₽\n3 месяца - {bot_config.param7}₽\n6 месяцев - {bot_config.param8}₽\n12 месяцев - {bot_config.param9}₽', reply_markup=nav.generate_payment_buttons(message.from_user.id))
            else:
                return 'error'
        if message.text == '📟 Инструкция':
            await bot.send_message(message.from_user.id, '📠 <b>Инструкция.</b>\n\nЕсли ты зашел в бота первый раз, то <b>жми</b>:\n\n• 💷 <b>Арендовать бота</b> - для покупки доступа ко всему функционалу бота (на 7 либо 30 дней).\n• 📆 <b>Тестовый период</b> - для активации тестового периода, он позволит тебе "попробовать" бота в течении 20 минут, без ограничений по функционалу.\n\nЕсли же ты уже оплатил аренду или активировал тестовый период, то жми:\n\n• 🎴 <b>Добавить пост</b> - для добавления нового поста из любого открытого канала в накрутку. Добавлять постов можно сколько угодно.\n• 🚦 <b>Управление накруткой</b> - для вывода списка постов, которые ты накручиваешь и удаления постов из списка накрутки.\n• 💷 <b>Управление арендой</b> - для продления срока аренды бота (на 7 либо 30 дней).', parse_mode="HTML")
        if message.text == '📆 Тестовый период':
            await bot.send_message(message.from_user.id, '📲Для получения тестового периода пишите @UFCMMATOP\n\n🕒 Время действия: 0 минут.')
        if message.text == '🚦 Управление накруткой':
            post_message, keyboard = nav.generate_postmenu(message.from_user.id)
            await bot.send_message(message.from_user.id, text=post_message, parse_mode="HTML", disable_web_page_preview=True)
        if message.text == '🎴 Добавить пост':
            await addPost.url.set()
            cancel_button = KeyboardButton('⏹ Отмена')
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(cancel_button)
            await bot.send_message(message.from_user.id, '🃏 Перешли мне пост из публичного канала:', reply_markup=keyboard)
        

@dp.message_handler(content_types=['any'], is_forwarded=True, state=addPost.url)
async def handle_forwarded_message(message: Message, state: FSMContext):
    status = db.check_status(message.from_user.id)[0]
    max_post = db.count_post(message.from_user.id)[0]
    if status == 1 and max_post < int(bot_config.param1):
        if message.forward_from_chat is not None:
            post_link = f"https://t.me/{message.forward_from_chat.username}/{message.forward_from_message_id}"
            await state.update_data({'url': post_link})
            await addPost.next()
            await message.reply(f'🕹 Введи максимальное число просмотров, при котором накрутка должна остановиться (до {bot_config.param2}):')
        else:
            await state.finish()
            await message.reply('Данное сообщение не является постом с канала!', reply_markup=nav.rental_kb)
    else:
        await state.finish()
        await message.reply(f'Максимальное количество постов равно {bot_config.param1}.', reply_markup=nav.rental_kb)


@dp.message_handler(state=addPost.amount)
async def load_post_amount(message: types.Message, state: FSMContext):
    amount = message.text
    if amount.isdigit():
        if int(amount) > 100 and int(amount) <= int(bot_config.param2):
            url = await state.get_data('url')
            url = url.get('url')
            await state.finish()
            order_id = api.order({'service': 2598, 'link': url, 'quantity': amount})
            db.add_post(order_id['order'], url, amount, message.from_user.id)
            db.increment_count_post()
            await bot.send_message(message.from_user.id, f'🎴 Пост {url} был успешно добавлен!', reply_markup=nav.rental_kb, disable_web_page_preview=True)
        else:
            await state.finish()
            await message.reply(f'🕹 Минимальное количество - 100, а максимальное - {bot_config.param2}', reply_markup=nav.rental_kb)
    else:
        await state.finish()
        await message.reply('Ошибка! Вы ввели неверное значение.', reply_markup=nav.rental_kb)

