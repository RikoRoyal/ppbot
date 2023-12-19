from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, KeyboardButton, \
    ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from db import DataBase

db = DataBase('db.db')

button_hi = KeyboardButton('💳 Баланс')
button_hi1 = KeyboardButton('👥 Рефералы')
button_hi2 = KeyboardButton('🔑 Обучение заработку')

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
greet_kb.add(button_hi)
greet_kb.add(button_hi1)
greet_kb.add(button_hi2)

balanceMenu = InlineKeyboardMarkup(row_width=2)
bal_1 = InlineKeyboardButton(text="🔻 Вывести", callback_data="bal_1")
balanceMenu.insert(bal_1)

adminsMenu = InlineKeyboardMarkup(row_width=2)
admins_1 = InlineKeyboardButton(text="✉️ Рассылка", callback_data="mail")
admins_2 = InlineKeyboardButton(text="📖 Меню каналов", callback_data="admin_2")
admins_3 = InlineKeyboardButton(text="📎 Меню ссылок", callback_data="admin_3")
admins_4 = InlineKeyboardButton(text="📎 Ссылка обучения", callback_data="admin_4")
admins_5 = InlineKeyboardButton(text="⚙️ Настройки", callback_data="admin_5")
admins_6 = InlineKeyboardButton(text="📤 Заявки на вывод", callback_data="admin_6")
adminsMenu.insert(admins_1)
adminsMenu.insert(admins_2)
adminsMenu.insert(admins_3)
adminsMenu.insert(admins_4)
adminsMenu.insert(admins_5)
adminsMenu.insert(admins_6)

channelsMenu = InlineKeyboardMarkup(row_width=2)
channelsAdd = InlineKeyboardButton(text="➕ Добавить", callback_data="channelsAdd")
channelsMin = InlineKeyboardButton(text="➖ Удалить", callback_data="channelsMin")
back = InlineKeyboardButton(text="◀️ Назад", callback_data="backAdm")
channelsMenu.insert(channelsAdd)
channelsMenu.insert(channelsMin)
channelsMenu.insert(back)

configMenu = InlineKeyboardMarkup(row_width=2)
EditConfBon = InlineKeyboardButton(text="✏️ Реф.бонус", callback_data="config_1")
EditConfMin = InlineKeyboardButton(text="✏️ Мин.выплата", callback_data="config_2")
back = InlineKeyboardButton(text="◀️ Назад", callback_data="backAdm")
configMenu.insert(EditConfBon)
configMenu.insert(EditConfMin)
configMenu.insert(back)

def showUrl():
    getUrl = InlineKeyboardMarkup(row_width=1)
    url = InlineKeyboardButton(text="✅ Пройти обучение", url=db.get_urls()[0])
    getUrl.insert(url)
    return getUrl

CCMenu = InlineKeyboardMarkup(row_width=2)
CCAdd = InlineKeyboardButton(text="➕ Добавить", callback_data="CCAdd")
CCMin = InlineKeyboardButton(text="➖ Удалить", callback_data="CCMin")
back = InlineKeyboardButton(text="◀️ Назад", callback_data="backAdm")
CCMenu.insert(CCAdd)
CCMenu.insert(CCMin)
CCMenu.insert(back)

def showChannels():
    keyboard = InlineKeyboardMarkup(row_width=1)
    channels = db.channels_get()
    for channel in channels:
        btn = InlineKeyboardButton(text=channel[0], url=channel[2])
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
        btn = InlineKeyboardButton(text=str(i) + " ❌", callback_data="delete_" + str(channel[3]))
        keyboard.insert(btn)
    btnDoneSub = InlineKeyboardButton(text="◀️ Назад", callback_data="backAdm")
    keyboard.insert(btnDoneSub)
    return keyboard

def showCCAdm():
    keyboard = InlineKeyboardMarkup(row_width=2)
    ccs = db.cc_get()
    i = 0
    for cc in ccs:
        i = i + 1
        btn = InlineKeyboardButton(text=str(i) + " ❌", callback_data="stop_" + str(cc[0]))
        keyboard.insert(btn)
    btnDoneSub = InlineKeyboardButton(text="◀️ Назад", callback_data="backAdm")
    keyboard.insert(btnDoneSub)
    return keyboard

def showCC():
    keyboard = InlineKeyboardMarkup(row_width=2)
    ccs = db.cc_get()
    i = 0
    for cc in ccs:
        i = i + 1
        btn = InlineKeyboardButton(text=str(i) + " 🎁", callback_data="box_" + str(cc[0]))
        keyboard.insert(btn)
    return keyboard
