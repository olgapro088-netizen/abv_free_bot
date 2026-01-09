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
        inlin
