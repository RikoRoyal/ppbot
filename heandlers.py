import hashlib
import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, KeyboardButton, \
    ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified
from main import bot, dp
from aiogram.types import Message, InputMediaPhoto, InputTextMessageContent, InlineQueryResultArticle, ChatActions
from aiogram import types, Dispatcher
from config import admins, not_sub_message, BOT_NICKNAME
import markups as nav
from db import DataBase
import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import admin, mail
import random

db = DataBase('db.db')

class viv_bal(StatesGroup):
    amounts = State()
    wallet = State()

async def send_to_admin(dp):
    try:
        i = 0
        for i in range(len(admins)):
            await bot.send_message(chat_id=admins[i], text='✅ Бот запущен')
    except Exception as e:
        pass

async def check_sub_channels(channels, user_id):
    channels = db.channels_get()
    for channel in channels:
        chat_member = await bot.get_chat_member(chat_id=channel[1], user_id=user_id)
        if chat_member['status'] == 'left':
            return False
    return True

@dp.message_handler(commands=['start'])
async def starting(message: Message):
    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            start_command = message.text
            referer_id = str(start_command[7:])
            if str(referer_id) != "":
                if str(referer_id) != str(message.from_user.id):
                    db.add_user(message.from_user.id, referer_id)
                    await bot.send_message(message.from_user.id, 'Привет <b>' + message.from_user.username + '</b>, добро пожаловать! 👋')
                    await bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
                    await asyncio.sleep(2.5)
                    await bot.send_message(message.from_user.id, '➖➖➖➖➖➖➖\n💰 Ваш баланс пополнен на <b>500₽</b>\n➖➖➖➖➖➖➖')
                    await bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
                    await asyncio.sleep(4.5)
                    img = open('1.gif', 'rb')
                    await bot.send_animation(message.from_user.id, img, None,  caption='<b>В качестве приветствия начислили Вам бонус 😌</b>\n\n🤚Чтобы продолжить, вам нужно всего лишь подписаться на 2 канала спонсора👇🏻✨', reply_markup=nav.showChannels())
                    try:
                        balance = db.get_balance_ref(referer_id)[0]
                        edit_balance = int(balance) + int(admin.updateConfig())
                        db.edit_balance_ref(edit_balance, referer_id)
                        balance = db.get_balance(message.from_user.id)[0]
                        edit_balance = int(balance) + 500
                        db.edit_balance(edit_balance, message.from_user.id)
                        await bot.send_message(referer_id, "🎁 У вас новый реферал! Вам было начислено {0}р за приглашенного вами друга)".format(admin.updateConfig()))
                    except Exception as e:
                        pass
                else:
                    db.add_user(message.from_user.id)
                    balance = db.get_balance(message.from_user.id)[0]
                    edit_balance = int(balance) + 500
                    db.edit_balance(edit_balance, message.from_user.id)
                    await bot.send_message(message.from_user.id, 'Привет <b>' + message.from_user.username + '</b>, добро пожаловать! 👋')
                    await bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
                    await asyncio.sleep(2.5)
                    await bot.send_message(message.from_user.id, '➖➖➖➖➖➖➖\n💰 Ваш баланс пополнен на <b>500₽</b>\n➖➖➖➖➖➖➖')
                    await bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
                    await asyncio.sleep(4.5)
                    img = open('1.gif', 'rb')
                    await bot.send_animation(message.from_user.id, img, None,  caption='<b>В качестве приветствия начислили Вам бонус 😌</b>\n\n🤚Чтобы продолжить, вам нужно всего лишь подписаться на 2 канала спонсора👇🏻✨', reply_markup=nav.showChannels())
            else:
                db.add_user(message.from_user.id)
                balance = db.get_balance(message.from_user.id)[0]
                edit_balance = int(balance) + 500
                db.edit_balance(edit_balance, message.from_user.id)
                await bot.send_message(message.from_user.id, 'Привет <b>' + message.from_user.username + '</b>, добро пожаловать! 👋')
                await bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
                await asyncio.sleep(2.5)
                await bot.send_message(message.from_user.id, '➖➖➖➖➖➖➖\n💰 Ваш баланс пополнен на <b>500₽</b>\n➖➖➖➖➖➖➖')
                await bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
                await asyncio.sleep(4.5)
                img = open('1.gif', 'rb')
                await bot.send_animation(message.from_user.id, img, None,  caption='<b>В качестве приветствия начислили Вам бонус 😌</b>\n\n🤚Чтобы продолжить, вам нужно всего лишь подписаться на 2 канала спонсора👇🏻✨', reply_markup=nav.showChannels())
        else:
            await bot.send_message(message.from_user.id, 'Привет <b>' + message.from_user.username + '</b>, добро пожаловать! 👋')
            await bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
            await asyncio.sleep(2.5)
            await bot.send_message(message.from_user.id, '➖➖➖➖➖➖➖\n💰 Ваш баланс пополнен на <b>500₽</b>\n➖➖➖➖➖➖➖')
            await bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
            await asyncio.sleep(4.5)
            img = open('1.gif', 'rb')
            await bot.send_animation(message.from_user.id, img, None,  caption='<b>В качестве приветствия начислили Вам бонус 😌</b>\n\n🤚Чтобы продолжить, вам нужно всего лишь подписаться на 2 канала спонсора👇🏻✨', reply_markup=nav.showChannels())

@dp.callback_query_handler(text_contains='subchannelDone')
async def subchannelDone(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    channels = db.channels_get()
    if await check_sub_channels(channels, call.from_user.id):
        img = open('1.jpg', 'rb')
        await bot.send_chat_action(call.from_user.id, ChatActions.TYPING)
        await asyncio.sleep(2)
        await bot.send_sticker(call.from_user.id, 'CAACAgIAAxkBAAEG30djnoMDD-09wYE2FBDYJ28xgwWugQAC1QUAAj-VzAr0FV2u85b8KCwE', reply_markup=nav.greet_kb)
        await bot.send_photo(call.from_user.id, img, caption='<b>Поздравляем! Вы участник розыгрыша ценных призов</b>\n\nЧтобы получить подарок, вам нужно открыть правильную коробочку Mystery Box', reply_markup=nav.showCC())
    else:
        await call.answer(text=not_sub_message, show_alert=True)
        await bot.send_message(call.from_user.id, '📝 <b>Для использования бота, вы должны быть подписаны на наши каналы:</b>', reply_markup=nav.showChannels())

@dp.callback_query_handler(text_contains='box', state=None)
async def geolocat(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data.split("_")[0] == 'box':
        id = call.data.split("_")[1]
        ccs = db.cc_result(id)
        for cc in ccs:
            keyboard = InlineKeyboardMarkup(row_width=1)
            btn = InlineKeyboardButton(text="🎁 Забрать подарок", url=cc[4])
            btnDoneSub = InlineKeyboardButton(text="◀️ Назад", callback_data="returnhome")
            keyboard.insert(btn)
            keyboard.insert(btnDoneSub)
            await bot.send_chat_action(call.from_user.id, ChatActions.TYPING)
            await asyncio.sleep(2)
            await bot.send_photo(call.from_user.id, cc[1], caption=cc[2] + "\n\n" + cc[3], reply_markup=keyboard)

@dp.callback_query_handler(text_contains='returnhome', state=None)
async def geolocat(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data == 'returnhome':
        img = open('1.jpg', 'rb')
        await bot.send_chat_action(call.from_user.id, ChatActions.TYPING)
        await asyncio.sleep(2)
        await bot.send_photo(call.from_user.id, img, caption='<b>Поздравляем! Вы участник розыгрыша ценных призов</b>\n\nЧтобы получить подарок, вам нужно открыть правильную коробочку Mystery Box', reply_markup=nav.showCC())

@dp.callback_query_handler(text_contains='bal', state=None)
async def geolocat(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data == 'bal_1':
        await bot.send_message(call.from_user.id,'✅ Введите сумму которую хотите вывести:\nДля отмены введите /cancel')
        await viv_bal.amounts.set()

@dp.message_handler(content_types=['text'], state=viv_bal.amounts)
async def load_text(message: types.Message, state:FSMContext):
    balance = db.get_balance(message.from_user.id)[0]
    amounts = message.text
    await state.update_data({'amounts': amounts})
    try:
        if type(int(amounts)) == int:
            if int(amounts) <= balance and int(amounts) >= admin.updateConfigOne():
                await bot.send_message(message.from_user.id, '🚀 Отлично! Теперь укажите номер вашего кошелька QIWI или Yoomoney или же Payeer')
                await viv_bal.next()
            else:
                await bot.send_message(message.from_user.id, '🚀 Ошибка! У вас не достаточно средств на балансе\nМинимальная сумма на вывод {0} рублей'.format(admin.updateConfigOne()))
                await state.finish()
    except Exception as e:
        await bot.send_message(message.from_user.id, '<b>Вы ввели информацию некорректно</b>.\n<b>Повторите попытку снова.</b>',
                               parse_mode='HTML')
        await state.finish()
        print(e)

@dp.message_handler(state=viv_bal.wallet)
async def load_user_id(message: types.Message, state: FSMContext):
    wallet = message.text
    amounts = await state.get_data('amounts')
    amounts = amounts.get('amounts')
    db.add_output(message.from_user.id, amounts, wallet)
    await bot.send_message(message.from_user.id, '🎁 Отлично! Ваша заявка на выплату была <b>успешно принята</b>! Ожидайте перевода средств в течение <b>48-часов</b>')
    try:
        balance = db.get_balance(message.from_user.id)[0]
        db.edit_balance(balance-int(amounts),message.from_user.id)
        statsv = db.get_vipl()[0]
        db.edit_vipl(statsv+int(amounts))
        await state.finish()
    except Exception as e:
        await state.finish()
        print(e)

@dp.message_handler(content_types=['text'], state=None)
async def text_menu(message: Message):
    if message.chat.type == 'private':
        if message.text == '👥 Рефералы':
            count_refc = db.count_referes(message.from_user.id)[0]
            await bot.send_message(message.from_user.id, '<b>👥 Партнёрская программа 👥</b>\n\n👤 Ваши приглашённые: <b>{0}</b>\n\n🔗 Ваша партнёрская ссылка: https://t.me/{1}?start={2}\n\n🤝 Приглашайте <b>друзей</b> и получайте за каждого <b>{3} рублей</b>.'.format(count_refc, BOT_NICKNAME,message.from_user.id, admin.updateConfig()), disable_web_page_preview=True)
        if message.text == '💳 Баланс':
            user_id = message.from_user.id
            balance = db.get_balance(message.from_user.id)[0]
            await bot.send_message(message.from_user.id, '💳 Ваш баланс: <b>{0}₽</b>'.format(balance), reply_markup=nav.balanceMenu)
        if message.text == '🔑 Обучение заработку':
            img = open('2.jpg', 'rb')
            await bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAEG-7BjpuryGXP9q3P7deuCj_qshxYb3QACAQADFm5MEh97vwZE6duLLAQ')
            await bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
            await asyncio.sleep(2)
            await bot.send_message(message.from_user.id, 'Привет <b>' + message.from_user.username + '</b>, я Чатикс и я проведу тебя в мир технологии искуственного интеллекта ✅ с <b>ГАРАНТИЕЙ результата!</b>\n\n🌟 <b>Новая ниша с низкой конкуренцией</b> 😊 вы сможете получать <b>ежедневно</b> от 3-5 тысяч рублей следуя нашим рекомендациям')
            await bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
            await asyncio.sleep(2)
            await bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAEG-7ljpuwigJpA4_qhNePMhVJGrmfM7AACayMAAulVBRhSEkehcyWEKiwE')
            await bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
            await asyncio.sleep(2)
            await bot.send_message(message.from_user.id, 'Зачисление на 💵 <b>+13 000₽</b> за 5 дней')
            await bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
            await asyncio.sleep(2)
            await bot.send_message(message.from_user.id, '<b>Наши ученики видят такие поступления регулярно, чем ты хуже?!</b>\n\nЗачисление на 💵 <b>+55 000₽</b> за 30 дней')
            await bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
            await asyncio.sleep(2)
            await bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAEG-71jpuyLGy6LOjtd2bTPb2-ds12eTgACCgADFm5MEro4tw8DwKEsLAQ')
            await bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
            await asyncio.sleep(2)
            await bot.send_message(message.from_user.id, '<b>После прохождения обучения ты сможешь зарабатывать:</b>\n\n до 💵 <b>+235299₽</b>\n\nПока другие о таком только мечтают, ты можешь начать воплощать это В реальность уже сейчас ... 😊', reply_markup=nav.showUrl())
            await bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
            await asyncio.sleep(2)
            await bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAEG-8Rjpuz3hSFN5mkKcQN7QLYW3vOgoQACHAADFm5MElhEbAvnYG3ALAQ')
            await bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
            await asyncio.sleep(2)
            await bot.send_message(message.from_user.id, '<b>Не страшно, если тебе тяжело дается обучение.</b>\n\nОбучение сделано на простом и понятном языке. Ты можешь проходить обучение в любом месте и когда тебе удобно. Для обучения и заработка тебе нужен будет телефон с выходом в интернет. 🚀\n\nНачать сейчас', reply_markup=nav.showUrl())
            await bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
            await asyncio.sleep(2)
            await bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAEG-8Zjpu1paGKMJySC7l-l_tSTQXX_IgACBAADFm5MEhNueNj6dWTdLAQ')
            await bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
            await asyncio.sleep(3)
            await bot.send_photo(message.from_user.id, img, caption='🎁 <b>АКЦИЯ 2022 года (с</b>\n💯 <b>100 ГАРАНТИЕЙ результата)</b>\n\nТвой ожидаемый доход через 1 день: 💵 <b>17181₽</b>\n\nПрямо сейчас ты можешь попасть на обучение всего за 1₽ с 💯 <b>ГАРАНТИЕЙ результата</b>\n\n<b>Жми 👇</b>', reply_markup=nav.showUrl())

def captch():
  numb_1 = random.randint(1, 10)
  numb_2 = random.randint(1, 10)

  itog = numb_1 + numb_2

  random_numbs = []
  while True:
    if len(random_numbs) == 5:
      break
    n1 = random.randint(1, 10)
    n2 = random.randint(1, 10)
    if n1 + n2 == itog:
      continue
    else:
      random_numbs.append(n1+n2)

  return numb_1, numb_2, itog, random_numbs
