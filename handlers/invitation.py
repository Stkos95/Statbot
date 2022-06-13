from aiogram.dispatcher import FSMContext
from keyboards.inline import kb_choice
from loader import dp
from aiogram import types






@dp.message_handler(commands=["statistic"], state=None)
async def choose_type_of_statistics(message: types.Message):
    await message.answer("Выбери тип статистики:", reply_markup=kb_choice)
    # await StatisticStates.First_state.set()