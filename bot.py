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
UA_TEMPLATE_2 = "https://abv-site.notion.site/UA-2c31d21a439980409644e61f9eeba247?pvs=73"

EN_TEMPLATE = "https://www.notion.so/Your-template-Goal-Check-10-Questions-EN-2c31d21a439980518e13d9a6444ee767?source=copy_link"

ABV_SHOWCASE = "https://abv-site.notion.site/2e31d21a43998011a8fcc3ead55994e7"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ------------------------
#   /start
# ------------------------
@dp.message(CommandStart())
async def start(message: types.Message):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇺🇦 Отримати українські шаблони", callback_data="get_ua")],
            [InlineKeyboardButton(text="🇬🇧 Get English template", callback_data="get_en")]
        ]
    )

    await message.answer(
        "🇺🇦 Вітаємо, з Вами ABV Простір 👋\n\n"
        "🇬🇧 Welcome, this is ABV Space 👋\n\n"
        "Оберіть, будь ласка, мову, щоб отримати шаблони ⬇️\n\n"
        "Please choose your language to get the template ⬇️",
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
#     Українські шаблони
# ------------------------
@dp.callback_query(lambda c: c.data == "get_ua")
async def choose_ua(callback: types.CallbackQuery):

    user_id = callback.from_user.id

    if await is_subscribed(user_id, UA_CHANNEL):
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📁 Шаблон перевірки цілі", url=UA_TEMPLATE)],
                [InlineKeyboardButton(text="📁 Фортеця ясності", url=UA_TEMPLATE_2)]
            ]
        )

        await callback.message.answer(
            "Дякуємо, що Ви вже з нами! 💛\nОберіть шаблон ⬇️",
            reply_markup=keyboard
        )

        keyboard_more = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text="✨ Переглянути всі шаблони ABV",
                    url=ABV_SHOWCASE
                )]
            ]
        )

        await callback.message.answer(
            "✨ Хочете більше?\n\n"
            "У ABV Просторі є готові системи:\n"
            "• фінанси\n"
            "• фокус і планування\n"
            "• робочі простори в Notion\n\n"
            "Це для тих, хто хоче не один шаблон,\n"
            "а систему під себе.",
            reply_markup=keyboard_more
        )
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📌 Підписатися на канал", url=f"https://t.me/{UA_CHANNEL[1:]}")],
            [InlineKeyboardButton(text="✅ Готово", callback_data="ua_ready")]
        ]
    )

    await callback.message.answer(
        "⚠️ Щоб отримати ці шаблони БЕЗКОШТОВНО, підпишіться на наш телеграм-канал.\n\n"
        "Після підписки натисніть кнопку:\n"
        "«✅ Готово»",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "ua_ready")
async def ua_ready(callback: types.CallbackQuery):

    user_id = callback.from_user.id

    if not await is_subscribed(user_id, UA_CHANNEL):
        await callback.answer("Ви ще не підписались 🙏", show_alert=True)
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📁 Шаблон перевірки цілі", url=UA_TEMPLATE)],
            [InlineKeyboardButton(text="📁 Фортеця ясності", url=UA_TEMPLATE_2)]
        ]
    )

    await callback.message.answer(
        "Дякуємо за підписку! 💛\nОберіть шаблон ⬇️",
        reply_markup=keyboard
    )

    keyboard_more = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="✨ Переглянути всі шаблони ABV",
                url=ABV_SHOWCASE
            )]
        ]
    )

    await callback.message.answer(
        "✨ Хочете більше?\n\n"
        "Це готові системи для життя й роботи в Notion.",
        reply_markup=keyboard_more
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
            "Thank you! Here is your template:",
            reply_markup=keyboard
        )
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📌 Subscribe to the channel", url=f"https://t.me/{EN_CHANNEL[1:]}")],
            [InlineKeyboardButton(text="✅ Done", callback_data="en_ready")]
        ]
    )

    await callback.message.answer(
        "To receive this template for free, please subscribe to our channel.",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "en_ready")
async def en_ready(callback: types.CallbackQuery):

    if not await is_subscribed(callback.from_user.id, EN_CHANNEL):
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
