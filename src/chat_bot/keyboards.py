from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

clear_context_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Очистить контекст"),]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
