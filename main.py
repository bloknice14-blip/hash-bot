import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()

# Пробуем найти токен в разных переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TOKEN") or os.getenv("TELEGRAM_TOKEN")

# 👇 АВАРИЙНЫЙ ВАРИАНТ: Если в Railway переменная упорно не подтягивается, 
# вставьте ваш токен от BotFather прямо в кавычки ниже:
FALLBACK_TOKEN = "" 

TOKEN_TO_USE = BOT_TOKEN if BOT_TOKEN else FALLBACK_TOKEN

if not TOKEN_TO_USE or TOKEN_TO_USE == "СЮДА_МОЖНО_ВСТАВИТЬ_ТОКЕН_ПРИ_ЖЕЛАНИИ":
    raise ValueError("❌ ОШИБКА: Токен не найден! Проверьте переменные в Railway.")

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN_TO_USE)
dp = Dispatcher()

# Ссылки и данные проекта HASHCOIN
CONTRACT_ADDRESS = "EQDHVvvLPQjoW5CFUHcIvWrKJf4ZTWyb_QpBvXR92g4drUgJ"
STONFI_URL = f"https://app.ston.fi/swap?chartVisible=true&ft=TON&tt={EQDHVvvLPQjoW5CFUHcIvWrKJf4ZTWyb_QpBvXR92g4drUgJ}"
DEDUST_URL = f"https://dedust.io/swap/TON/{EQDHVvvLPQjoW5CFUHcIvWrKJf4ZTWyb_QpBvXR92g4drUgJ}"
CHANNEL_URL = "https://t.me/hashua_ua"


def get_main_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💎 Купить на STON.fi", url=STONFI_URL),
                InlineKeyboardButton(text="ᯤ Купить на DeDust.io", url=DEDUST_URL)
            ],
            [
                InlineKeyboardButton(text="📢 Официальный канал", url=CHANNEL_URL)
            ],
            [
                InlineKeyboardButton(text="ℹ️ О проекте / Контракт", callback_data="info")
            ]
        ]
    )


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    welcome_text = (
        "<b>Добро пожаловать в официальный инфо-хаб HASHCOIN!</b> 🚀\n\n"
        "Здесь вы можете быстро перейти к покупке токена на децентрализованных биржах."
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard(), parse_mode="HTML")


@dp.callback_query(F.data == "info")
async def show_info(callback: types.CallbackQuery):
    info_text = (
        "<b>Информация о проекте HASHCOIN:</b>\n\n"
        f"📋 <b>Адрес смарт-контракта:</b>\n<code>{CONTRACT_ADDRESS}</code>"
    )
    back_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="◀️ Назад", callback_data="back_home")]]
    )
    await callback.message.edit_text(info_text, reply_markup=back_keyboard, parse_mode="HTML")
    await callback.answer()


@dp.callback_query(F.data == "back_home")
async def back_home(callback: types.CallbackQuery):
    welcome_text = "<b>Добро пожаловать в официальный инфо-хаб HASHCOIN!</b> 🚀"
    await callback.message.edit_text(welcome_text, reply_markup=get_main_keyboard(), parse_mode="HTML")
    await callback.answer()


async def main():
    logging.basicConfig(level=logging.INFO)
    print("Бот HASHCOIN успешно запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
