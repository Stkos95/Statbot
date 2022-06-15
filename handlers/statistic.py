from aiogram import types
from loader import dp
from processing.count_statistic_after_match import operating_func
from processing.savetoExcel import create_template_of_excel
from keyboards.kb_fabric import statistic_callback
from list_of_actions import act
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from states import SummaryStates
from processing.transfer_result import transfer_results
from aiogram.dispatcher import FSMContext

from config import admin
import datetime

import os


def kb_1_summary(datas, key=None):
    key_1 = InlineKeyboardMarkup(row_width=2)
    for j in datas:
        d = InlineKeyboardButton(text=f"{j} ({datas[j]})",
                                 callback_data=statistic_callback.new(action=j, team=1 if not key else 2))
        key_1.insert(d)
    return key_1


@dp.callback_query_handler(text="summary")
async def request_statistic(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    async with state.proxy() as data:
        data['Команда 1'] = act()
        data['Команда 2'] = act()
        # data['result'] = {}
        print(data['Команда 2'])
        print(type(data['Команда 2']))
        await call.message.answer("Вы решили считать общую послематчевую статистику...\nВот клавиатура...",
                                  reply_markup=kb_1_summary(data['Команда 1']))
        await call.message.answer("Для второй", reply_markup=kb_1_summary(data['Команда 2'], 2))
    await call.message.answer(text="Для продолжения нажмите на клавиатуре 'Второй'",
                              reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text="Второй")))
    await SummaryStates.First_state.set()


@dp.callback_query_handler(statistic_callback.filter(team="1"),
                           state=[SummaryStates.First_state, SummaryStates.Second_state])
async def count_statistic_1(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    value = callback_data['action']
    async with state.proxy() as data:
        operating_func(data=data['Команда 1'], value=value)
        await call.message.edit_reply_markup(reply_markup=kb_1_summary(data['Команда 1']))
    await call.answer("work")


@dp.callback_query_handler(statistic_callback.filter(team="2"),
                           state=[SummaryStates.First_state, SummaryStates.Second_state])
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
        data["result_1"] = {}
        data["result_1"]["1"] = data['Команда 1']
        data["result_1"]["2"] = data['Команда 2']
        data['Команда 1'] = act()
        data['Команда 2'] = act()
        await message.answer("Первый тайм закончен, ниже клавиатура для второго тайма:\n для ПЕРВОЙ КОМАНДЫ!!!",
                             reply_markup=kb_1_summary(data['Команда 1']))
        await message.answer("Для второй команды:", reply_markup=kb_1_summary(data['Команда 2'], 2))
        await SummaryStates.Second_state.set()


@dp.message_handler(text="Готово", state=SummaryStates.Second_state)
async def ready(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        first_half_result = data["result_1"]
        second_half_result = {}
        second_half_result["1"] = data['Команда 1']
        second_half_result["2"] = data['Команда 2']

    name = 'final test'
    data_first_half = transfer_results(first_half_result)
    data_second_half = transfer_results(second_half_result)
    create_template_of_excel(name=f"{name}.xls", data_half_one=data_first_half, data_half_two=data_second_half)
    print(1111111)

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
