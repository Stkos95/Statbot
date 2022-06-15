from aiogram import types
from loader import dp
from other.other_functions import operating_func
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
from pprint import pprint


def kb_1_summary(datas, key=None):
    key_1 = InlineKeyboardMarkup(row_width=2)
    for j in datas:
        d = InlineKeyboardButton(text=f"{j} ({datas[j]})", callback_data=statistic_callback.new(action=j, team=1 if not key else 2))
        key_1.insert(d)
    return key_1


@dp.callback_query_handler(text="summary")
async def request_statistic(call: types.CallbackQuery, state: FSMContext):
    actions = get_actions_for_counting()
    print(actions)
    await call.answer()
    async with state.proxy() as data:
        data['Команда 1'] = actions.team_one
        data['Команда 2'] = actions.team_two
        data['result'] = {}
        print(data['Команда 2'])
        print(type(data['Команда 2']))
        await call.message.answer("Вы решили считать общую послематчевую статистику...\nВот клавиатура...", reply_markup=kb_1_summary(data['Команда 1']))
        await call.message.answer("Для второй", reply_markup=kb_1_summary(data['Команда 2'], 2))
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
        await call.message.edit_reply_markup(reply_markup=kb_1_summary(data['Команда 2'], 2))
    await call.answer("work")

@dp.message_handler(text="Второй", state=SummaryStates.First_state)
async def second_half(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["result"]["1 half"] = {}
        data["result"]["1 half"]["1"] = data['Команда 1']
        data["result"]["1 half"]["2"] = data['Команда 2']
        data['Команда 1'] = get_actions_for_counting().team_one
        data['Команда 2'] = get_actions_for_counting().team_two
        await message.answer("Первый тайм закончен, ниже клавиатура для второго тайма:\n для ПЕРВОЙ КОМАНДЫ!!!", reply_markup=kb_1_summary(data['Команда 1']))
        await message.answer("Для второй команды:", reply_markup=kb_1_summary(data['Команда 2'],2))

@dp.message_handler(text="Готово",state=SummaryStates.First_state)
async def ready(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["result"]["2 half"] = {}
        data["result"]["2 half"]["1"] = data['Команда 1']
        data["result"]["2 half"]["2"] = data['Команда 2']
        pprint(data["result"])
        results = data["result"]

    # datas = finalResults(results)
    # pprint(datas)

    # name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    #
    # with open(f"jsonFiles/{name}.json", "w",encoding="UTF-8") as js:
    #     json.dump(new_actions_summary, js, ensure_ascii=False)
    #     print(name)
    #
    #
    # await dp.bot.send_message(chat_id=admin, text="сейчас отправят файл!!")
    # await dp.bot.send_document(chat_id=admin, document=open(f"jsonFiles/{name}.json", "rb"))
    # d = len(os.listdir("jsonFiles/"))
    # if d >= 3:
    #     await dp.bot.send_message(chat_id=admin, text=f"Уже скопилось {d} файлов, может пора их удалить?")
    # await state.finish()


