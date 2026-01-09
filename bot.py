import asyncio
import os
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ------------------------
# Налаштування
# ------------------------
UA_CHANNEL = "@abvprostir"
EN_CHANNEL = "@abvspace_en"

UA_TEMPLATE_1 = "https://www.notion.so/UA-2c31d21a43998006a631cb6c928090a9"
UA_TEMPLATE_2 = "https://abv-site.notion.site/UA-2c31d21a439980409644e61f9eeba247"
EN_TEMPLATE = "https://www.notion.so/Your-template-Goal-Check-10-Questions-EN-2c31d21a439980518e13d9a6444ee767"
ABV_SHOWCASE = "https://abv-site.notion.site/2e31d21a43998011a8fcc3ead55994e7"

# 🔴 ВСТАВ СЮДИ ПОВНИЙ URL З /exec
GOOGLE_SHEETS_WEBHOOK = "https://script.google.com/macros/s/AKfycbyfR8rlQWo6_exuMo9yLIRKAjX0imrH9JK_-NO565FRUXW0JSPgIcIDX8gFoCF4B82m-Q/exec"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ------------------------
# Аналітика
# ------------------------
async def log_click(user_id: int, action: str, lang: str):
    async with aiohttp.ClientSession() as session:
        await session.post(
            GOOGLE_SHEETS_WEBHOOK,
            json={
                "user_id": user_id,
                "action": action,
                "lang": lang
            }
        )

# ------------------------
# Перевірка підписки
# ------------------------
async def is_subscribed(user_id, channel):
    try:
        member = await bot.get_chat_member(channel, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# ------------------------
# /start
# ------------------------
@dp.message(CommandStart())
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇺🇦 Українські шаблони", callback_data="get_ua")],
            [InlineKeyboardButton(text="🇬🇧 English template", callback_data="get_en")]
        ]
    )

    await message.answer(
        "Вітаю 👋 Це ABV Простір / ABV Space\n\n"
        "Оберіть мову, щоб отримати шаблони ⬇️",
        reply_markup=keyboard
    )

# ------------------------
# UA FLOW
# ------------------------
@dp.callback_query(lambda c: c.data == "get_ua")
async def get_ua(callback: types.CallbackQuery):
    if await is_subscribed(callback.from_user.id, UA_CHANNEL):
        await show_ua_templates(callback)
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📌 Підписатися", url=f"https://t.me/{UA_CHANNEL[1:]}")],
                [InlineKeyboardButton(text="✅ Готово", callback_data="ua_ready")]
            ]
        )
        await callback.message.answer(
            "Щоб отримати шаблони безкоштовно — підпишіться на канал ⬇️",
            reply_markup=keyboard
        )

@dp.callback_query(lambda c: c.data == "ua_ready")
async def ua_ready(callback: types.CallbackQuery):
    if not await is_subscribed(callback.from_user.id, UA_CHANNEL):
        await callback.answer("Ще не підписались 🙏", show_alert=True)
        return
    await show_ua_templates(callback)

async def show_ua_templates(callback):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📁 Шаблон перевірки цілі", callback_data="ua_t1")],
            [InlineKeyboardButton(text="📁 Фортеця ясності", callback_data="ua_t2")],
            [InlineKeyboardButton(text="✨ Всі шаблони ABV", callback_data="ua_showcase")]
        ]
    )
    await callback.message.answer(
        "Оберіть шаблон ⬇️",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "ua_t1")
async def ua_t1(callback: types.CallbackQuery):
    await log_click(callback.from_user.id, "ua_template_1", "UA")
    await callback.message.answer(f"📁 Шаблон ⬇️\n{UA_TEMPLATE_1}")

@dp.callback_query(lambda c: c.data == "ua_t2")
async def ua_t2(callback: types.CallbackQuery):
    await log_click(callback.from_user.id, "ua_template_2", "UA")
    await callback.message.answer(f"📁 Шаблон ⬇️\n{UA_TEMPLATE_2}")

@dp.callback_query(lambda c: c.data == "ua_showcase")
async def ua_showcase(callback: types.CallbackQuery):
    await log_click(callback.from_user.id, "showcase", "UA")
    await callback.message.answer(f"✨ Всі шаблони ABV ⬇️\n{ABV_SHOWCASE}")

# ------------------------
# EN FLOW
# ------------------------
@dp.callback_query(lambda c: c.data == "get_en")
async def get_en(callback: types.CallbackQuery):
    if await is_subscribed(callback.from_user.id, EN_CHANNEL):
        await send_en_template(callback)
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📌 Subscribe", url=f"https://t.me/{EN_CHANNEL[1:]}")],
                [InlineKeyboardButton(text="✅ Done", callback_data="en_ready")]
            ]
        )
        await callback.message.answer(
            "Subscribe to get the template ⬇️",
            reply_markup=keyboard
        )

@dp.callback_query(lambda c: c.data == "en_ready")
async def en_ready(callback: types.CallbackQuery):
    if not await is_subscribed(callback.from_user.id, EN_CHANNEL):
        await callback.answer("Not subscribed yet 🙏", show_alert=True)
        return
    await send_en_template(callback)

async def send_en_template(callback):
    await log_click(callback.from_user.id, "en_template", "EN")
    await callback.message.answer(f"📁 Template ⬇️\n{EN_TEMPLATE}")

# ------------------------
# RUN
# ------------------------
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
