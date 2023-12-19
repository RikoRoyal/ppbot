from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, KeyboardButton, \
    ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from utils.db import DataBase
import hashlib
import secrets
from config import merchant_id, secret_word, BotConfig
from utils.api import Api

bot_config = BotConfig()
bot_config.load_from_database()

api = Api()

db = DataBase('db.db')

def showChannels(user_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    channels = db.channels_get()
    for channel in channels:
        btn = InlineKeyboardButton(text=channel[2], url=channel[3])
        keyboard.insert(btn)
        btnDoneSub = InlineKeyboardButton(text="✔️ Я ПОДПИСАЛСЯ ✔️", callback_data="subchannelDone")
        keyboard.insert(btnDoneSub)
    return keyboard

def showChannelsAdm():
    keyboard = InlineKeyboardMarkup(row_width=2)
    channels = db.channels_get()
    i = 0
    for channel in channels:
        i = i + 1
        btn = InlineKeyboardButton(text=str(i) + " ❌", callback_data="delete_" + str(channel[1]))
        keyboard.insert(btn)
    return keyboard

def generate_payment_link(merchant_id, secret_word, order_id, amount, currency, us_login):
    sign_string = f"{merchant_id}:{amount}:{secret_word}:{currency}:{order_id}"
    sign = hashlib.md5(sign_string.encode()).hexdigest()
    payment_link = f"https://pay.freekassa.ru/?m={merchant_id}&oa={amount}&o={order_id}&s={sign}&currency={currency}&us_login={us_login}&lang=ru"
    return payment_link

def generate_postmenu(user_id):
    order_ids = db.get_orderId(user_id)
    inline_buttons = []
    for order_id in order_ids:
        inline_buttons.append(InlineKeyboardButton('Удалить', callback_data='delete_' + str(order_id[0])))

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*inline_buttons)

    post_count = len(order_ids)
    post_message = f"Найдено {post_count} постов:\n"

    for i, order_id in enumerate(order_ids, start=1):
        url = db.get_orderUrl(order_id[0])
        remains = api.status(order_id[0])['remains']
        post_message += f"{i}. <a href=\"{url[0][0]}\">Пост</a>: <b>осталось</b> - {remains}\n"

    return post_message, keyboard


button_texts = ['💷 Арендовать бота', '📆 Тестовый период', '👥 Рефералы', '📟 Инструкция']
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
greet_kb.add(*[KeyboardButton(text) for text in button_texts])

rental_texts = ['🎴 Добавить пост', '🚦 Управление накруткой', '💷 Управление арендой', '👥 Рефералы', '📟 Инструкция']
rental_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
rental_kb.add(*[KeyboardButton(text) for text in rental_texts])

admins_buttons = [
    InlineKeyboardButton(text=btn_text, callback_data=f"admin_{i+1}")
    for i, btn_text in enumerate(["✉️ Рассылка", "👀 Посты", "📆 Выдать тест", "📢 Каналы", "⚙️ Настройки"])
]
adminsMenu = InlineKeyboardMarkup(row_width=2).add(*admins_buttons)

config_buttons = [
    InlineKeyboardButton(text=btn_text, callback_data=f"config_{i+1}")
    for i, btn_text in enumerate(["Max Post", "Limit Post", "Price 1", "Price 2", "Price 3", "Price 4", "Price 5", "Price 6", "Price 7"])
]
configMenu = InlineKeyboardMarkup(row_width=2).add(*config_buttons)

def generate_payment_buttons(users_id):
    bot_config.load_from_database()
    random_data = secrets.token_hex(16)
    hash_object = hashlib.sha256(random_data.encode())
    order_id = hash_object.hexdigest()[:8]
    payment_buttons = [
        InlineKeyboardButton(text=btn_text, url=btn_url)
        for btn_text, btn_url in [
            ("💳 Оплатить день", generate_payment_link(merchant_id, secret_word, '1 day_' + order_id, str(bot_config.param3), 'RUB', users_id)),
            ("💳 Оплатить 3 дня", generate_payment_link(merchant_id, secret_word, '3 day_' + order_id, str(bot_config.param4), 'RUB', users_id)),
            ("💳 Оплатить 7 дней", generate_payment_link(merchant_id, secret_word, '1 week_' + order_id, str(bot_config.param5), 'RUB', users_id)),
            ("💳 Оплатить месяц", generate_payment_link(merchant_id, secret_word, '1 month_' + order_id, str(bot_config.param6), 'RUB', users_id)),
            ("💳 Оплатить 3 месяца", generate_payment_link(merchant_id, secret_word, '3 months_' + order_id, str(bot_config.param7), 'RUB', users_id)),
            ("💳 Оплатить 6 месяцев", generate_payment_link(merchant_id, secret_word, '6 months_' + order_id, str(bot_config.param8), 'RUB', users_id)),
            ("💳 Оплатить 12 месяцев", generate_payment_link(merchant_id, secret_word, '12 months_' + order_id, str(bot_config.param9), 'RUB', users_id))
            ]
        ]
    paymentMenu = InlineKeyboardMarkup(row_width=2).add(*payment_buttons)
    return paymentMenu

channels_buttons = [
    InlineKeyboardButton(text=btn_text, callback_data=f"channels_{i+1}")
    for i, btn_text in enumerate(["➕ Добавить", "➖ Удалить"])
]
channelsMenu = InlineKeyboardMarkup(row_width=2).add(*channels_buttons)

def generate_postmenuAdm(page=1, per_page=30):
    order_ids = db.get_orderAll()

    post_count = len(order_ids)
    post_message = f"Найдено {post_count} постов:\n"

    start_index = (page - 1) * per_page
    end_index = start_index + per_page

    for i, order_id in enumerate(order_ids[start_index:end_index], start=start_index+1):
        url = db.get_orderUrl(order_id[0])
        remains = api.status(order_id[0])['remains']
        post_message += f"{i}. <a href=\"{url[0][0]}\">Пост</a>: <b>осталось</b> - {remains}\n"

    keyboard = InlineKeyboardMarkup(row_width=1)
    if post_count > per_page:
        total_pages = (post_count + per_page - 1) // per_page
        current_page = page

        if current_page > 1:
            keyboard.add(
                InlineKeyboardButton(
                    'Предыдущая страница',
                    callback_data=f'prev_page:{current_page-1}'
                )
            )
        if current_page < total_pages:
            keyboard.add(
                InlineKeyboardButton(
                    'Следующая страница',
                    callback_data=f'next_page:{current_page+1}'
                )
            )

    return post_message, keyboard