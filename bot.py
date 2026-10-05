import asyncio
import html
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# === НАСТРОЙКИ ===
BOT_TOKEN = "8638427778:AAHt7qRGrjXNGwDIBUpHHx3KC5VN6zy7q9Y"
GROUP_ID = -5484859150

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Отправь мне название песни и исполнителя, либо ссылку на трек из YouTube / TikTok, "
        "и я передам твоё предложение в группу!"
    )

@dp.message(F.text)
async def handle_music_request(message: types.Message):
    # Игнорируем сообщения, отправленные внутри самой группы
    if message.chat.id == GROUP_ID:
        return

    # Экранируем текст от пользователя, чтобы спецсимволы (<, >, &) не ломали HTML
    raw_text = message.text.strip()
    safe_text = html.escape(raw_text)
    
    user = message.from_user
    username = f"@{user.username}" if user.username else html.escape(user.full_name)

    formatted_msg = (
        f"📌 <b>Содержание:</b>\n{safe_text}\n\n"
        f"👤 <b>Отправлено от:</b> {username} (ID: <code>{user.id}</code>)"
    )

    # Кнопка для быстрого перехода к диалогу с отправителем
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💬 Написать автору", url=f"tg://user?id={user.id}")]
        ]
    )

    try:
        await bot.send_message(
            chat_id=GROUP_ID,
            text=formatted_msg,
            parse_mode="HTML",  # Меняем Markdown на HTML
            reply_markup=kb
        )
        await message.reply("✅ Отлично! Твой запрос отправлен в группу.")
    except Exception as e:
        logging.error(f"Ошибка отправки в группу: {e}")
        await message.reply("❌ Произошла ошибка при отправке запроса. Попробуйте позже.")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())