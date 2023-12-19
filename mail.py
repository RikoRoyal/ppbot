from main import bot, dp
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from db import DataBase
from config import admins
import time

db = DataBase('db.db')

class MailerStates(StatesGroup):
    manage_mailer = State()
    mailer_text = State()
    add_media = State()
    add_inline_links = State()

add_media_mailer_button = InlineKeyboardButton('Добавить медиа', callback_data='add_media_mailer')
add_inline_link_mailer_button = InlineKeyboardButton('Добавить инлайн ссылку', callback_data='add_inline_link_mailer')
send_mailer_button = InlineKeyboardButton('Отправить рассылку', callback_data='start_mailer')
cancel_button_adm = InlineKeyboardButton('Отмена', callback_data='cancel')
manage_mailer_inline_kb = InlineKeyboardMarkup().add(add_media_mailer_button).add(add_inline_link_mailer_button).add(send_mailer_button).add(cancel_button_adm)


@dp.callback_query_handler(state="*", text="cancel")
async def close_inline(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Отменено')
    await state.finish()

@dp.callback_query_handler(text_contains='mail')
async def geolocat(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id in admins and call.data == 'mail':
        bot_message = await bot.send_message(call.from_user.id, "Введите текст для рассылки:", reply_markup=cancel_button_adm)
        await state.update_data(bot_message=bot_message)
        await MailerStates.mailer_text.set()


@dp.message_handler(state=MailerStates.mailer_text)
async def mailer_set_text(message: types.Message, state: FSMContext):
    await message.delete()
    ids = db.get_all_id()
    text = message.html_text
    await state.update_data(text=text)
    data = await state.get_data()
    bot_message = data['bot_message']
    links = data.get('inline_links', None)
    media = data.get('media_type', None)

    if links is not None:
        links = '\n\n'.join([f'{links.get(link)}\n{link}' for link in links])
    await bot_message.edit_text(f'Количество пользователей: {len(ids)}\n'
                                f'Текст: {text}\n'
                                f'Медиа: {media}\n'
                                f'Ссылки:\n{links}', reply_markup=manage_mailer_inline_kb)
    await MailerStates.manage_mailer.set()


@dp.callback_query_handler(text='add_media_mailer', state=MailerStates.manage_mailer)
async def add_media_mailer(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    data = await state.get_data()
    await callback_query.message.edit_text('Отправьте медиа:\nДоступные виды: фото, видео, голосовое сообщение, файл')
    await MailerStates.add_media.set()


@dp.callback_query_handler(text='add_inline_link_mailer',
                           state=MailerStates.manage_mailer)
async def add_media_mailer(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    data = await state.get_data()
    await callback_query.message.edit_text(
        'Отправьте ссылки и текст для инлайн кнопок разделяя их <b>;</b> а кнопки - новой строкой\n'
        'Например:\n'
        'text;link\ntext2;link2')
    await MailerStates.add_inline_links.set()




@dp.message_handler(state=MailerStates.add_inline_links)
async def add_inline_links(message: types.Message, state: FSMContext):
    await message.delete()
    links = {}
    links_text = message.text.split('\n')
    for i in links_text:
        i = i.split(';')
        links.update({i[1]: i[0]})
    await state.update_data(inline_links=links)
    data = await state.get_data()
    ids = db.get_all_id()
    bot_message = data['bot_message']
    text = data['text']
    links = data.get('inline_links', None)
    media = data.get('media_type', None)

    if links is not None:
        links = '\n\n'.join([f'{links.get(link)}\n{link}' for link in links])
    await bot_message.edit_text(f'Количество пользователей: {len(ids)}\n'
                                f'Текст: {text}\n'
                                f'Медиа: {media}\n'
                                f'Ссылки:\n{links}', reply_markup=manage_mailer_inline_kb)
    await MailerStates.manage_mailer.set()


@dp.message_handler(content_types=['photo', 'video', 'voice', 'document'],
                    state=MailerStates.add_media)
async def add_media(message: types.Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    if message.photo:
        await state.update_data(media_type='photo')
        await state.update_data(media_id=message.photo[0].file_id)
    if message.video:
        await state.update_data(media_type='video')
        await state.update_data(media_id=message.video.file_id)
    if message.document:
        await state.update_data(media_type='document')
        await state.update_data(media_id=message.document.file_id)
    if message.voice:
        await state.update_data(media_type='voice')
        await state.update_data(media_id=message.voice.file_id)
    data = await state.get_data()
    ids = db.get_all_id()
    bot_message = data['bot_message']
    text = data['text']
    links = data.get('inline_links', None)
    media = data.get('media_type', None)
    if links is not None:
        links = '\n\n'.join([f'{links.get(link)}\n{link}' for link in links])
    await bot_message.edit_text(f'Количество пользователей: {len(ids)}\n'
                                f'Текст: {text}\n'
                                f'Медиа: {media}\n'
                                f'Ссылки:\n{links}', reply_markup=manage_mailer_inline_kb)
    await MailerStates.manage_mailer.set()


@dp.callback_query_handler(text='start_mailer', state=MailerStates.manage_mailer)
async def start_mailer(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    ids = db.get_all_id()
    bot_message = data['bot_message']
    text = data['text']
    links = data.get('inline_links', None)
    media_type = data.get('media_type', None)
    media_id = data.get('media_id', None)
    if links is not None:
        kb = InlineKeyboardMarkup()
        for i in links:
            kb.add(InlineKeyboardButton(text=links.get(i), url=i))
    else:
        kb = None
    if media_type is None:
        send_mail = bot.send_message
    elif media_type == 'photo':
        send_mail = bot.send_photo
    elif media_type == 'video':
        send_mail = bot.send_video
    elif media_type == 'voice':
        send_mail = bot.send_voice
    elif media_type == 'document':
        send_mail = bot.send_document

    await bot_message.edit_text('Успешно')
    correct = 0
    failed = 0
    bot_message = await bot.send_message(callback_query.from_user.id, f'<b>Рассылка</b>:\n'
                                                                      f'Отправлено: <code>{correct}</code>\n'
                                                                      f'Не отправлено: <code>{failed}</code>')
    start_time = time.time()
    await state.finish()
    for id_ in ids:
        try:
            if media_type != None:
                await send_mail(id_[0], media_id, caption=text, reply_markup=kb)
            else:
                await bot.send_message(id_[0], text, reply_markup=kb)
        except Exception:
            failed += 1
        else:
            correct += 1
        await asyncio.sleep(.05)
    await bot_message.edit_text(
        f'<b>Рассылка закончена за {int((time.time() - start_time) / 60)} мин. {round(time.time() - start_time - int((time.time() - start_time) / 60) * 60, 1)} сек.</b>\n'
        f'Отправлено: <code>{correct}</code>\n'
        f'Не отправлено: <code>{failed}</code>\n'
        f'Всего: <code>{correct + failed}</code>')
