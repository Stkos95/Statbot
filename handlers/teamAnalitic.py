from loader import dp
from aiogram import types
from states import StatisticStates
from aiogram.dispatcher import FSMContext
from config import actions_team_analitic
from keyboards.kb_fabric import team_analitic_callback
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup,KeyboardButton


def kb_1_analitic(data):
    key_1_analitic = InlineKeyboardMarkup(row_width=2)
    for i in data:
        new_button = InlineKeyboardButton(text=f"{i} ({data[i]})", callback_data=team_analitic_callback.new(i))
        key_1_analitic.insert(new_button)
    return key_1_analitic





@dp.callback_query_handler(text="team_analitic", state=StatisticStates.First_state)
async def team_statistic(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['Первый тайм'] = actions_team_analitic["Первый тайм"]
        data['Второй тайм'] = actions_team_analitic["Второй тайм"]
        await call.message.answer("Вы решили считать командную аналитику...\nВот клавиатура...", reply_markup=kb_1_analitic(data['Первый тайм']))
        await call.message.answer("Для перехода на 2 тайм, выберите второй тайм", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text="Второй тайм")))
    await StatisticStates.First_state.set()





@dp.callback_query_handler(team_analitic_callback.filter(), state= StatisticStates.First_state)
async def team_statistic_count(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    new_value = callback_data["analitic_actions"]
    async with state.proxy() as data:
        for i in data["Первый тайм"]:
            if new_value == i:
                data["Первый тайм"][i] += 1
        await call.message.edit_reply_markup(reply_markup=kb_1_analitic(data['Первый тайм']))
    await call.answer("work")


@dp.message_handler(text="Второй тайм", state= StatisticStates.First_state)
async def team_statistic_count(message: types.Message, state: FSMContext):
    async with state.proxy() as data:

        await message.answer("Клавиатура для второго тайма:", reply_markup=kb_1_analitic(data['Второй тайм']))
        await message.answer("Для Завершения выберите 'Готово'",
                                  reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
                                      KeyboardButton(text="Завершить")))

    await StatisticStates.next()



@dp.callback_query_handler(team_analitic_callback.filter(), state= StatisticStates.Second_state)
async def team_statistic_count(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    new_value = callback_data["analitic_actions"]
    async with state.proxy() as data:
        for i in data["Второй тайм"]:
            if new_value == i:
                data["Второй тайм"][i] += 1
        await call.message.edit_reply_markup(reply_markup=kb_1_analitic(data['Второй тайм']))
    await call.answer("work")

@dp.message_handler(text="Завершить", state= StatisticStates.Second_state)
async def team_statistic_count_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        new_analitic_actions = {"Первый тайм" : data["Первый тайм"],
                                "Второй тайм" : data["Второй тайм"]}

    await state.finish()
    print(new_analitic_actions)


