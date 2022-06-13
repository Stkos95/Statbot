from aiogram import types
from loader import dp
from other.other_functions import operating_func
from keyboards.inline import kb_choice
from keyboards.kb_fabric import statistic_callback
from list_of_actions import get_actions_for_counting
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup,KeyboardButton
from states import SummaryStates
from aiogram.dispatcher import FSMContext
import openpyxl
from config import actions_summary
from config import admin
import datetime
import json
import os





def kb_1_summary(datas):
    key_1 = InlineKeyboardMarkup(row_width=2)

    for j in datas:


        d = InlineKeyboardButton(text=f"{j} ({datas[j]})", callback_data=statistic_callback.new(action=j, team=1))
        key_1.insert(d)

    return key_1

def kb_2_summary(datas):
    key_2 = InlineKeyboardMarkup(row_width=2)
    for i in datas:
        dd = InlineKeyboardButton(text=f"{i} ({datas[i]})", callback_data=statistic_callback.new(action=i, team=2))
        key_2.insert(dd)

    return key_2



"""
Перенес в файл приветствия
"""
# @dp.message_handler(commands=["statistic"], state=None)
# async def choose_type_of_statistics(message: types.Message, state: FSMContext):
#     await message.answer("Выбери тип статистики:", reply_markup=kb_choice)
#     # await StatisticStates.First_state.set()




@dp.callback_query_handler(text="summary")
async def request_statistic(call: types.CallbackQuery, state: FSMContext):
    actions = get_actions_for_counting()
    print(actions)
    await call.answer()
    async with state.proxy() as data:
        data['Команда 1'] = actions.team_one
        data['Команда 2'] = actions.team_two
        print(data['Команда 2'])
        print(type(data['Команда 2']))
        await call.message.answer("Вы решили считать общую послематчевую статистику...\nВот клавиатура...", reply_markup=kb_1_summary(data['Команда 1']))
        await call.message.answer("Для второй", reply_markup=kb_2_summary(data['Команда 2']))
    await call.message.answer(text = "Для продолжения нажмите на клавиатуре 'Второй'",reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text="Второй")))
    await SummaryStates.First_state.set()



@dp.callback_query_handler(statistic_callback.filter(team="1"), state=SummaryStates.First_state)
async def count_statistic_1(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    value = callback_data['action']
    async with state.proxy() as data:
        operating_func(data=data['Команда 1'], value=value)
        await call.message.edit_reply_markup(reply_markup=kb_1_summary(data['Команда 1']))
    await call.answer("work")


@dp.callback_query_handler(statistic_callback.filter(team="2"), state=SummaryStates.First_state)
async def count_statistic_2(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    value = callback_data['action']
    print(callback_data)
    async with state.proxy() as data:
        operating_func(data=data['Команда 2'], value=value)
        await call.message.edit_reply_markup(reply_markup=kb_2_summary(data['Команда 2']))
    await call.answer("work")

@dp.message_handler(text="Второй", state=SummaryStates.First_state)
async def second_half(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["result"] = {}



    global new_actions_summary
    new_actions_summary = {
        "Первый тайм": {
            "Команда 1": {},
            "Команда 2": {}
        },
        "Второй тайм": {
            "Команда 1": {},
            "Команда 2": {}
        }
    }
    async with state.proxy() as data:
        new_actions_summary["Первый тайм"]["Команда 1"] = data['Команда 1']
        new_actions_summary["Первый тайм"]["Команда 2"] = data['Команда 2']
        data['Команда 1'] = actions_summary["Второй тайм"]["Команда 1"]
        data['Команда 2'] = actions_summary["Второй тайм"]["Команда 2"]


        await message.answer("Первый тайм закончен, ниже клавиатура для второго тайма:\n для ПЕРВОЙ КОМАНДЫ!!!", reply_markup=kb_1_summary(data['Команда 1']))
        await message.answer("Для второй команды:", reply_markup=kb_2_summary(data['Команда 2']))
    await SummaryStates.next()


@dp.callback_query_handler(statistic_callback.filter(), state=SummaryStates.Second_state)
async def count_statistic(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    value = callback_data['action']
    async with state.proxy() as data:
        check_1time = data['Команда 1']
        check_2time = data['Команда 2']
        if value.startswith("1"):

            for i in check_1time:
                if i == value:
                    data['Команда 1'][i] += 1

            await call.message.edit_reply_markup(reply_markup=kb_1_summary(data['Команда 1']))
        elif value.startswith("2"):

            for i in check_2time:
                if i == value:
                    data['Команда 2'][i] += 1

            await call.message.edit_reply_markup(reply_markup=kb_2_summary(data['Команда 2']))

    await call.answer("work_1")





@dp.message_handler(text="Готово",state=SummaryStates.Second_state)
async def ready(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        new_actions_summary["Второй тайм"]["Команда 1"] = data['Команда 1']
        new_actions_summary["Второй тайм"]["Команда 2"] = data['Команда 2']



    name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    with open(f"jsonFiles/{name}.json", "w",encoding="UTF-8") as js:
        json.dump(new_actions_summary, js, ensure_ascii=False)
        print(name)


    await dp.bot.send_message(chat_id=admin, text="сейчас отправят файл!!")
    await dp.bot.send_document(chat_id=admin, document=open(f"jsonFiles/{name}.json", "rb"))
    d = len(os.listdir("jsonFiles/"))
    if d >= 3:
        await dp.bot.send_message(chat_id=admin, text=f"Уже скопилось {d} файлов, может пора их удалить?")
    await state.finish()