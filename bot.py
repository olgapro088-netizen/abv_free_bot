import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Канали
UA_CHANNEL = "@abvprostir"
EN_CHANNEL = "@abvspace_en"

# Лінки шаблонів
UA_TEMPLATE = "https://www.notion.so/UA-2c31d21a43998006a631cb6c928090a9?source=copy_link"
EN_TEMPLATE = "https://www.notion.so/Your-template-Goal-Check-10-Questions-EN-2c31d21a439980518e13d9a6444ee767?source=copy_link"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ------------------------
#   /start
# ------------------------
@dp.message(CommandStart())
async def start(message: types.Message):

    logo_path = "logo.png"
    photo = FSInputFile(logo_path)

    # Кнопки вибору мови
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇺🇦 Отримати український шаблон", callback_data="get_ua")],
            [InlineKeyboardButton(text="🇬🇧 Get English template", callback_data="get_en")]
        ]
    )

    caption_text = (
        "🇺🇦 Вітаємо, з Вами ABV Простір 👋\n\n"
        "🇬🇧 Welcome, this is ABV Space 👋"
    )

    await message.answer_photo(photo=photo, caption=caption_text)

    await message.answer(
        "Оберіть, будь ласка, мову, щоб отримати свій шаблон ⬇️\n\n"
        "Please choose your language to get your template ⬇️",
        reply_markup=keyboard
    )


# ------------------------
#   Перевірка підписки
# ------------------------
async def is_subscribed(user_id, channel):
    try:
        member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# ------------------------
#     Український шаблон
# ------------------------
@dp.callback_query(lambda c: c.data == "get_ua")
async def choose_ua(callback: types.CallbackQuery):

    user_id = callback.from_user.id

    if await is_subscribed(user_id, UA_CHANNEL):
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="📁 Отримати шаблон", url=UA_TEMPLATE)]]
        )
        await callback.message.answer(
            "Дякуємо, що Ви вже з нами! 💛\nОсь Ваш шаблон:",
            reply_markup=keyboard
        )
        return

    text = (
        "⚠️ Щоб отримати цей шаблон БЕЗКОШТОВНО, підпишіться на наш телеграм-канал.\n\n"
        "ℹ️ У каналі ми публікуємо корисні поради та рекомендації по Notion,\n"
        "анонси нових шаблонів та пропозицій.\n\n"
        "Після підписки натисніть кнопку:\n"
        "«✅ Готово»"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📌 Підписатися на канал", url=f"https://t.me/{UA_CHANNEL[1:]}")],
            [InlineKeyboardButton(text="✅ Готово", callback_data="ua_ready")]
        ]
    )

    await callback.message.answer(text, reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == "ua_ready")
async def ua_ready(callback: types.CallbackQuery):

    user_id = callback.from_user.id

    if not await is_subscribed(user_id, UA_CHANNEL):
        await callback.answer("Ви ще не підписались 🙏", show_alert=True)
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="📁 Отримати шаблон", url=UA_TEMPLATE)]]
    )

    await callback.message.answer(
        "Дякуємо за підписку! Ось Ваш шаблон ⬇️",
        reply_markup=keyboard
    )


# ------------------------
#     English Template
# ------------------------
@dp.callback_query(lambda c: c.data == "get_en")
async def choose_en(callback: types.CallbackQuery):

    user_id = callback.from_user.id

    if await is_subscribed(user_id, EN_CHANNEL):

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="📁 Get the template", url=EN_TEMPLATE)]]
        )

        await callback.message.answer(
            "Thank you! You are already subscribed 💛\nHere is your template:",
            reply_markup=keyboard
        )
        return

    text = (
        "⚠️ To receive this template FOR FREE, please subscribe to our Telegram channel.\n\n"
        "ℹ️ In the channel, we post helpful Notion tips, recommendations,\n"
        "announcements of new templates and special offers.\n\n"
        "After subscribing, press:\n"
        "«✅ Done»"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📌 Subscribe to the channel", url=f"https://t.me/{EN_CHANNEL[1:]}")],
            [InlineKeyboardButton(text="✅ Done", callback_data="en_ready")]
        ]
    )

    await callback.message.answer(text, reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == "en_ready")
async def en_ready(callback: types.CallbackQuery):

    user_id = callback.from_user.id

    if not await is_subscribed(user_id, EN_CHANNEL):
        await callback.answer("You are not subscribed yet 🙏", show_alert=True)
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="📁 Get the template", url=EN_TEMPLATE)]]
    )

    await callback.message.answer(
        "Thank you for subscribing! Here is your template ⬇️",
        reply_markup=keyboard
    )


# ------------------------
#    RUN
# ------------------------
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
