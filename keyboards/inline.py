from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.kb_fabric import statistic_callback

statistickb = InlineKeyboardMarkup(row_width=1,inline_keyboard=[
    [
        InlineKeyboardButton(text="Удар точный",callback_data=statistic_callback.new(action="shoot_correct")),
        InlineKeyboardButton(text="Удар МИМО",callback_data=statistic_callback.new(action="shoot_fault"))
    ]
])


kb_choice = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="Послематчевое табло", callback_data="summary"),
        InlineKeyboardButton(text="Командная аналитика", callback_data="team_analitic")
    ]
])