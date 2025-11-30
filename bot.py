import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Канали
UA_CHANNEL = "@avbprostir"
EN_CHANNEL = "@abvspace_en"

UA_TEMPLATE_LINK = "https://www.notion.so/notiocraft/2bbb3b25b5c8809c80cbd9635662345b?source=copy_link"
EN_TEMPLATE_LINK = "https://www.notion.so/notiocraft/2bbb3b25b5c8809ca4dbd959476eb7d5?source=copy_link"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ---------- START ----------
@dp.message(CommandStart())
async def start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="🇺🇦 Отримати український шаблон", callback_data="choose_ua")
    builder.button(text="🇬🇧 Get English template", callback_data="choose_en")
    builder.adjust(1)

    await message.answer_photo(
        photo="https://i.imgur.com/5vcgCcK.png",  # Твоє лого, завантажене на Imgur
        caption="Привіт! Обери мову, щоб отримати свій шаблон 👇",
        reply_markup=builder.as_markup()
    )

# ---------- ПЕРЕХІД UA або EN ----------
@dp.callback_query(lambda c: c.data in ["choose_ua", "choose_en"])
async def choose_language(callback: types.CallbackQuery):
    choice = callback.data

    if choice == "choose_ua":
        await ask_to_subscribe(callback, language="ua")
    else:
        await ask_to_subscribe(callback, language="en")

# ---------- ПРОСИМО ПІДПИСАТИСЯ ----------
async def ask_to_subscribe(callback, language):
    builder = InlineKeyboardBuilder()

    if language == "ua":
        builder.button(text="Підписатися на канал 🇺🇦", url=f"https://t.me/{UA_CHANNEL[1:]}")
        builder.button(text="Я підписався ✔️", callback_data="check_ua")
        text = "Будь ласка, підпишись на канал, щоб отримати шаблон:"
    else:
        builder.button(text="Subscribe to EN Channel 🇬🇧", url=f"https://t.me/{EN_CHANNEL[1:]}")
        builder.button(text="I subscribed ✔️", callback_data="check_en")
        text = "Please subscribe to the channel to get your template:"

    builder.adjust(1)
    await callback.message.answer(text, reply_markup=builder.as_markup())


# ---------- ПЕРЕВІРКА ПІДПИСКИ ----------
async def is_subscribed(user_id, channel):
    try:
        member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

@dp.callback_query(lambda c: c.data in ["check_ua", "check_en"])
async def check_subscription(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    check_type = callback.data

    if check_type == "check_ua":
        subscribed = await is_subscribed(user_id, UA_CHANNEL)
        if subscribed:
            await callback.message.answer(f"Дякую за підписку! Ось твій шаблон:👇\n\n{UA_TEMPLATE_LINK}")
        else:
            await callback.message.answer("Підписку не знайдено 😢\nСпробуй ще раз.")
    else:
        subscribed = await is_subscribed(user_id, EN_CHANNEL)
        if subscribed:
            await callback.message.answer(f"Thanks for subscribing! Here is your template 👇\n\n{EN_TEMPLATE_LINK}")
        else:
            await callback.message.answer("Subscription not detected 😢\nTry again.")

# ---------- RUN ----------
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
