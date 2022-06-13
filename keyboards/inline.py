from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.kb_fabric import statistic_callback


kb_choice = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="Послематчевое табло", callback_data="summary"),
        InlineKeyboardButton(text="Командная аналитика", callback_data="team"),
        InlineKeyboardButton(text="Персональная статистика", callback_data="personal")
    ]
])