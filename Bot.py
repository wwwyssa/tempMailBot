from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, \
    KeyboardButton
from aiogram.client.default import DefaultBotProperties
import asyncio
import html
from tempMailRequests import create_temp_email, get_emails

import logging
logging.basicConfig(level=logging.INFO)

API_TOKEN = ''

bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

user_emails = {}
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/create_email")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Бот для создания временной почты.\n", reply_markup=keyboard
    )

@dp.message(Command("create_email"))
async def cmd_create_email(message: Message):
    email = await create_temp_email()
    if email:
        user_emails[message.from_user.id] = email
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Проверить письма", callback_data="check_emails")]
            ]
        )
        await message.answer(
            f"Ваша временная почта: <code>{html.escape(email)}</code>\n"
            "Нажмите кнопку ниже, чтобы проверить письма.",
            reply_markup=keyboard
        )
    else:
        await message.answer(
            "Не удалось создать временную почту. Попробуйте позже."
        )

@dp.callback_query(lambda query: query.data == "check_emails")
async def process_check_emails(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    if user_id in user_emails:
        email = user_emails[user_id]

        emails = await get_emails(email)
        if emails:
            response = "Ваши письма:\n\n"
            for email in emails:
                escaped_from = html.escape(email['from'])
                escaped_subject = html.escape(email['subject'])
                escaped_body = html.escape(email['body_text'])
                response += (
                    f"<b>От:</b> {escaped_from}\n"
                    f"<b>Тема:</b> {escaped_subject}\n"
                    f"<b>Текст:</b> {escaped_body}\n"

                )
                response +="\n" + "-" * 40 + "\n"
            await callback_query.message.answer(response)
        else:
            await callback_query.message.answer("Писем нет.")
    else:
        await callback_query.message.answer("Временная почта не найдена.")

    await callback_query.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())