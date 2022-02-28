from aiogram import types
from loader import dp
from keyboards.inline import kb_choice
from keyboards.kb_fabric import statistic_callback

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from states import StatisticStates
from aiogram.dispatcher import FSMContext
import openpyxl
from config import actions_summary
from config import admin
import datetime
import json

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




def kb_1_summary(datas):
    key_1 = InlineKeyboardMarkup(row_width=2)

    for j in datas:

        if j.startswith('1'):
            d = InlineKeyboardButton(text=f"{j} ({datas[j]})", callback_data=statistic_callback.new(j))
            key_1.insert(d)

    return key_1

def kb_2_summary(datas):
    key_2 = InlineKeyboardMarkup(row_width=2)
    for i in datas:
        if i.startswith('2'):
            dd = InlineKeyboardButton(text=f"{i} ({datas[i]})", callback_data=statistic_callback.new(f"{i}"))
            key_2.insert(dd)

    return key_2




@dp.message_handler(commands=["statistic"], state=None)
async def choose_type_of_statistics(message: types.Message, state: FSMContext):
    await message.answer("Выбери тип статистики:", reply_markup=kb_choice)
    await StatisticStates.First_state.set()




@dp.callback_query_handler(text="summary", state=StatisticStates.First_state)
async def request_statistic(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['Команда 1'] = actions_summary["Первый тайм"]["Команда 1"]
        data['Команда 2'] = actions_summary["Первый тайм"]["Команда 2"]
        await call.message.answer("Вы решили считать статистику...\nВот клавиатура...", reply_markup=kb_1_summary(data['Команда 1']))
        await call.message.answer("Для второй", reply_markup=kb_2_summary(data['Команда 2']))
    await StatisticStates.First_state.set()

@dp.callback_query_handler(statistic_callback.filter(), state=StatisticStates.First_state)
async def count_statistic(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    value = callback_data['action']
    async with state.proxy() as data:
        check_1time = data['Команда 1']
        check_2time = data['Команда 2']
        if value.startswith("1"):

            for i in check_1time:

                if i == value:
                    data['Команда 1'][i] +=1

            await call.message.edit_reply_markup(reply_markup=kb_1_summary(data['Команда 1']))
        elif value.startswith("2"):

            for i in check_2time:
                if i == value:
                    data['Команда 2'][i] +=1

            await call.message.edit_reply_markup(reply_markup=kb_2_summary(data['Команда 2']))

    await call.answer("work")


@dp.message_handler(text="Второй", state=StatisticStates.First_state)
async def second_half(message: types.Message, state: FSMContext):
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
    await StatisticStates.next()


@dp.callback_query_handler(statistic_callback.filter(), state=StatisticStates.Second_state)
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





@dp.message_handler(text="Готово",state=StatisticStates.Second_state)
async def ready(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        new_actions_summary["Второй тайм"]["Команда 1"] = data['Команда 1']
        new_actions_summary["Второй тайм"]["Команда 2"] = data['Команда 2']



    name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    with open(f"{name}.json", "w",encoding="UTF-8") as js:
        json.dump(new_actions_summary, js, ensure_ascii=False)
        print(name)


    await dp.bot.send_message(chat_id=admin, text="сейчас отправят файл!!")
    await dp.bot.send_document(chat_id=admin, document=open(f"{name}.json", "rb"))
    await state.finish()