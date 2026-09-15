import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

# Загружаем переменные окружения (если используется .dotenv локально)
load_dotenv()

# Безопасное получение токена бота из переменных окружения (Railway)
BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ ОШИБКА: Токен бота не найден в переменных окружения (BOT_TOKEN)!")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Адрес смарт-контракта и полностью сформированные ссылки на пулы
CONTRACT_ADDRESS = "EQDHVvvLPQjoW5CFUHcIvWrKJf4ZTWyb_QpBvXR92g4drUgJ"
STONFI_URL = f"https://app.ston.fi/swap?chartVisible=true&ft=TON&tt={CONTRACT_ADDRESS}"
DEDUST_URL = f"https://dedust.io/swap/TON/{CONTRACT_ADDRESS}"
CHANNEL_URL = "https://t.me/hashua_ua"  # Замените на ссылку вашего реального канала, если нужно


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
