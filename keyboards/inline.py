from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.kb_fabric import statistic_callback

statistickb = InlineKeyboardMarkup(row_width=1,inline_keyboard=[
    [
        InlineKeyboardButton(text="Удар точный",callback_data=statistic_callback.new(action="shoot_correct")),
        InlineKeyboardButton(text="Удар МИМО",callback_data=statistic_callback.new(action="shoot_fault"))
    ]
])