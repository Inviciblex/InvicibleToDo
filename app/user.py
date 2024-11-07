from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart

from app.database.requests import set_user, del_task, set_task
import app.keyboards as kb
from config import admin_id, TOKEN

bot = Bot(token=TOKEN)

user = Router()


@user.message(CommandStart())
async def cmd_start(message: Message):
    await set_user(message.from_user.id, message.from_user.username)
    await message.answer(f"Привет, {message.from_user.first_name}! 👋\n\n"
                         '➕ Для добавления задачи напиши ее в чат.\n\n'
                         '➖ Для удаления просто нажми на нее.',
                         reply_markup=await kb.tasks(message.from_user.id))


@user.callback_query(F.data.startswith('task_'))
async def delete_task(callback: Message):
    await callback.answer('🎉 Задача выполнена!')
    await del_task(callback.data.split('_')[1])
    await callback.message.edit_text('➕ Для добавления новой напиши ее в чат.\n\n'
                                     '➖ Для удаления нажми на задачу.',
                                     reply_markup=await kb.tasks(callback.from_user.id))


@user.message()
async def add_task(message: Message):
    await message.delete()
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=int(message.message_id - 1))
    except:
        pass
    if message.text == '/db':
        user_id = message.from_user.id
        if user_id == admin_id:
            file = FSInputFile('db.sqlite3')
            await message.answer_document(file)
            return

    try:
        if len(message.text) > 100:
            await message.answer('Слишком длинная задача!')
            return
        await set_task(message.from_user.id, message.text)
        await message.answer('✨ Задача добавлена!\n\n'
                             '➕ Для добавления новой напиши ее в чат.\n'
                             '➖ Для удаления нажми на задачу.',
                             reply_markup=await kb.tasks(message.from_user.id))
    except:
        await message.answer('⚠️ Ошибка обработки. Бот работает только с текстом.\n'
                             'Введи новую задачу для продолжения работы')
