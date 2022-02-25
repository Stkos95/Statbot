from aiogram import types
from loader import dp
from keyboards.inline import statistickb
from keyboards.kb_fabric import statistic_callback

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from states import StatisticStates
from aiogram.dispatcher import FSMContext
import openpyxl
from config import first_time_dict, second_time_dict, actions
from pprint import pprint


new_actions = {
    "Первый тайм": {
        "Команда 1": {},
        "Команда 2": {}
    },
    "Второй тайм": {
        "Команда 1": {},
        "Команда 2": {}
    }
}

def kb_1(datas,num):
    key_1 = InlineKeyboardMarkup(row_width=2)

    for j in datas:

        if j.startswith('1'):
            d = InlineKeyboardButton(text=f"{j} ({datas[j]})", callback_data=statistic_callback.new(j))
            key_1.insert(d)

    return key_1

def kb_2(datas):
    key_2 = InlineKeyboardMarkup(row_width=2)
    for i in datas:
        if i.startswith('2'):
            dd = InlineKeyboardButton(text=f"{i} ({datas[i]})", callback_data=statistic_callback.new(f"{i}"))
            key_2.insert(dd)

    return key_2


@dp.message_handler(commands=["statistic"], state=None)
async def request_statistic(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Команда 1'] = actions["Первый тайм"]["Команда 1"]
        data['Команда 2'] = actions["Первый тайм"]["Команда 2"]
        await message.answer("Вы решили считать статистику...\nВот клавиатура...",reply_markup=kb_1(data['Команда 1'],1))
        await message.answer("Для второй", reply_markup=kb_2(data['Команда 2']))
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

            await call.message.edit_reply_markup(reply_markup=kb_1(data['Команда 1'],1))
        elif value.startswith("2"):

            for i in check_2time:
                if i == value:
                    data['Команда 2'][i] +=1

            await call.message.edit_reply_markup(reply_markup=kb_2(data['Команда 2']))

    await call.answer("work")


@dp.message_handler(text="Второй", state=StatisticStates.First_state)
async def second_half(message: types.Message, state: FSMContext):
    global new_actions
    new_actions = {
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
        new_actions["Первый тайм"]["Команда 1"] = data['Команда 1']
        new_actions["Первый тайм"]["Команда 2"] = data['Команда 2']
        data['Команда 1'] = actions["Второй тайм"]["Команда 1"]
        data['Команда 2'] = actions["Второй тайм"]["Команда 2"]

        pprint(new_actions)

        await message.answer("Первый тайм закончен, ниже клавиатура для второго тайма:\n для ПЕРВОЙ КОМАНДЫ!!!",reply_markup=kb_1(data['Команда 1'],2))
        await message.answer("Для второй команды:", reply_markup=kb_2(data['Команда 2']))
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

            await call.message.edit_reply_markup(reply_markup=kb_1(data['Команда 1'], 1))
        elif value.startswith("2"):

            for i in check_2time:
                if i == value:
                    data['Команда 2'][i] += 1

            await call.message.edit_reply_markup(reply_markup=kb_2(data['Команда 2']))

    await call.answer("work_1")





@dp.message_handler(text="Готово",state=StatisticStates.Second_state)
async def ready(message: types.Message, state: FSMContext):
     async with state.proxy() as data:
        new_actions["Второй тайм"]["Команда 1"] = data['Команда 1']
        new_actions["Второй тайм"]["Команда 2"] = data['Команда 2']
        pprint(new_actions)


        # text = ['Ваша статистика:']
        # text.append("За первый тайм: ")
        # print(data)
        # first_time_itog = data["Первый тайм"]
        # second_time_itog = data["Второй тайм"]
        # for i in first_time_itog :
        #     text.append(f"{i} : {first_time_itog[i]}")
        # text.append("За второй тайм: ")
        # for i in second_time_itog:
        #     text.append(f"{i} : {second_time_itog[i]}")
        #
        #
        # await message.answer(text="\n".join(text))
        #
        #
        # itog = {}
        #
        # itog["первый тайм"] = first_time_itog






