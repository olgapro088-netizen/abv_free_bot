import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@avbprostir"   # Канал для перевірки підписки
DOWNLOAD_LINK = "https://your-download-link.com/file.pdf"  # Сюди вставиш свій файл

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# --- Кнопки ---
def subscribe_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="📢 Підписатися на канал", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
    kb.button(text="🔄 Перевірити підписку", callback_data="check")
    kb.adjust(1)
    return kb.as_markup()


def download_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="⬇️ Завантажити файл", url=DOWNLOAD_LINK)
    return kb.as_markup()


# --- Команда START ---
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Привіт! 👋\n\nЩоб отримати доступ до файлу, підпишись на канал:",
        reply_markup=subscribe_keyboard()
    )


# --- Перевірка підписки ---
@dp.callback_query(lambda c: c.data == "check")
async def check_subscription(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)

        if member.status in ["member", "creator", "administrator"]:
            await callback.message.edit_text(
                "🎉 Дякую за підписку!\nОсь твоє посилання:",
                reply_markup=download_keyboard()
            )
        else:
            await callback.answer("❗ Ви ще не підписані", show_alert=True)

    except Exception:
        await callback.answer("Помилка. Спробуйте ще раз.", show_alert=True)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
