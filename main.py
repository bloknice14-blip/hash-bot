import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- ВАШИ ССЫЛКИ И ДАННЫЕ ---
CONTRACT_ADDRESS = "EQDHVvvLPQjoW5CFUHcIvWrKJf4ZTWyb_QpBvXR92g4drUgJ"
STONFI_POOL_URL = f"https://app.ston.fi/swap?chartVisible=true&ft=TON&tt=EQDHVvvLPQjoW5CFUHcIvWrKJf4ZTWyb_QpBvXR92g4drUgJ"
CHANNEL_URL = "https://t.me/hashua_ua"  # <--- Сюда вставьте ссылку на ваш канал

# --- КЛАВИАТУРА МЕНЮ ---
def get_main_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💎 Купить HASHCOIN (STON.fi)", url=STONFI_POOL_URL)],
            [InlineKeyboardButton(text="📢 Наш Telegram-канал", url=CHANNEL_URL)],
            [InlineKeyboardButton(text="📜 О монете и контракте", callback_data="about_token")]
        ]
    )

def get_back_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="back_home")]
        ]
    )

# --- ХЕНДЛЕРЫ ---

@dp.message(Command("start"))
async def cmd_start(message: Message):
    # Картинка-баннер (замените ссылку на свою, когда будет готова)
    photo_url = "https://via.placeholder.com/600x300.png?text=HASHCOIN+Hub"
    
    caption = (
        f"👋 Привет, <b>{message.from_user.first_name}</b>!\n\n"
        f"Добро пожаловать в официальный бот проекта <b>HASHCOIN</b> в сети TON.\n\n"
        f"Используйте кнопки ниже для перехода в пулы ликвидности и следите за новостями комьюнити!"
    )
    
    await message.answer_photo(
        photo=photo_url,
        caption=caption,
        parse_mode="HTML",
        reply_markup=get_main_keyboard()
    )

@dp.callback_query(F.data == "back_home")
async def back_home(callback: Message):
    await callback.message.edit_caption(
        caption="Главное меню HASHCOIN:",
        parse_mode="HTML",
        reply_markup=get_main_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data == "about_token")
async def show_about(callback: Message):
    text = (
        f"📌 <b>Информация о HASHCOIN:</b>\n\n"
        f"• <b>Сеть:</b> TON\n"
        f"• <b>Адрес контракта:</b>\n<code>{CONTRACT_ADDRESS}</code>\n\n"
        f"<i>Используйте этот адрес для импорта токена в кошелек.</i>"
    )
    await callback.message.edit_caption(
        caption=text,
        parse_mode="HTML",
        reply_markup=get_back_keyboard()
    )
    await callback.answer()

async def main():
    print("Простой бот HASHCOIN успешно запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())