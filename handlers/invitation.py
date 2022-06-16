from aiogram.dispatcher import FSMContext
from keyboards.inline import kb_choice
from loader import dp
from aiogram import types
from states.fsm import SummaryStates, PersonalStatisticStates, TeamAnalytic
from keyboards.kb_fabric import chooce_type_callback




@dp.message_handler(commands=["statistic"], state=None)
async def choose_type_of_statistics(message: types.Message):
    await message.answer("Выбери тип статистики:", reply_markup=kb_choice)
    # await SummaryStates.First_state.set()

@dp.callback_query_handler(chooce_type_callback.filter(), state=None)
async def request_statistic(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    kind = callback_data['type']
    print(kind)
    await call.message.answer('Укажите название файла:')
    match kind:
        case "summary":
            await SummaryStates.Zero_state.set()
        case "team":
            await TeamAnalytic.Zero_state.set()
        case "personal":
            await PersonalStatisticStates.Zero_state.set()








