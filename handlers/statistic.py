from aiogram import types
from loader import dp
from processing.count_statistic_after_match import operating_func
from processing.savetoExcel_summary import create_template_of_excel
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

@dp.message_handler(state=SummaryStates.Zero_state)
async def description(message: types.Message, state: FSMContext):
    await message.answer('Укажи опознавательные знаки для обоих команд:')
    async with state.proxy() as data:
        data['name'] = message.text
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

        name = data['name']
    data_first_half = transfer_results(first_half_result)
    data_second_half = transfer_results(second_half_result)
    create_template_of_excel(name=f"./excel files completed/{name}.xls", data_half_one=data_first_half, data_half_two=data_second_half)





    await dp.bot.send_message(chat_id=admin, text="сейчас отправят файл!!")
    await dp.bot.send_document(chat_id=admin, document=open(f"./excel files completed/{name}.xls", "rb"))
    await state.finish()


@dp.message_handler(state=SummaryStates.First_state)
async def request_statistic(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Команда 1'] = act()
        data['Команда 2'] = act()
        print(data['Команда 2'])
        print(type(data['Команда 2']))
        await message.answer(message.text)
        await message.answer("Вы решили считать общую послематчевую статистику...\nВот клавиатура...",
                                  reply_markup=kb_1_summary(data['Команда 1']))
        await message.answer("Для второй", reply_markup=kb_1_summary(data['Команда 2'], 2))
    await message.answer(text="Для продолжения нажмите на клавиатуре 'Второй'",
                              reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text="Второй")))


@dp.message_handler(text='Отмена' ,state='*')
async def cancel(message: types.Message, state: FSMContext):
    await message.answer("Отменено!")
    await state.finish()