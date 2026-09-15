import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

# Загружаем переменные окружения (для локального запуска)
load_dotenv()

# Получаем и проверяем токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ ОШИБКА: Не найден BOT_TOKEN в переменных окружения!")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Ссылки и данные проекта HASHCOIN
CONTRACT_ADDRESS = "EQDHVvvLPQjoW5CFUHcIvWrKJf4ZTWyb_QpBvXR92g4drUgJ"
STONFI_URL = f"https://app.ston.fi/swap?chartVisible=true&ft=TON&tt={CONTRACT_ADDRESS}"
DEDUST_URL = f"https://dedust.io/swap/TON/{CONTRACT_ADDRESS}"
CHANNEL_URL = "https://t.me/ваш_канал"  # Замените на ссылку вашего реального канала


# Главное меню с кнопками
def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(
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
    return keyboard


# Команда /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    welcome_text = (
        "<b>Добро пожаловать в официальный инфо-хаб HASHCOIN!</b> 🚀\n\n"
        "Здесь вы можете быстро и безопасно перейти к покупке токена на децентрализованных биржах TON-экосистемы, "
        "а также следить за новостями проекта."
    )
    
    # Если у вас есть картинка-баннер, можете отправлять ее через send_photo, 
    # а пока используем обычное текстовое сообщение с кнопками:
    await message.answer(welcome_text, reply_markup=get_main_keyboard(), parse_mode="HTML")


# Обработка нажатия на кнопку "О проекте"
@dp.callback_query(F.data == "info")
async def show_info(callback: types.CallbackQuery):
    info_text = (
        "<b>Информация о проекте HASHCOIN:</b>\n\n"
        f"📋 <b>Адрес смарт-контракта:</b>\n<code>{CONTRACT_ADDRESS}</code>\n\n"
        "Используйте только проверенные ссылки из этого бота для обмена!"
    )
    
    # Кнопка возврата назад в главное меню
    back_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="◀️ Назад", callback_data="back_home")]
        ]
    )
    
    await callback.message.edit_text(info_text, reply_markup=back_keyboard, parse_mode="HTML")
    await callback.answer()


# Возврат в главное меню по инлайн-кнопке
@dp.callback_query(F.data == "back_home")
async def back_home(callback: types.CallbackQuery):
    welcome_text = (
        "<b>Добро пожаловать в официальный инфо-хаб HASHCOIN!</b> 🚀\n\n"
        "Выберите нужное действие ниже:"
    )
    await callback.message.edit_text(welcome_text, reply_markup=get_main_keyboard(), parse_mode="HTML")
    await callback.answer()


# Запуск процесса поллинга
async def main():
    logging.basicConfig(level=logging.INFO)
    print("Бот HASHCOIN успешно запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
