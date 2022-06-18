import datas
from loader import dp
from aiogram import types
from states import PersonalStatisticStates
from aiogram.dispatcher import FSMContext
from keyboards.kb_fabric import personal_callback
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from config import admin
from list_of_actions import get_zone_actions, get_other_actions, get_shoots_actions
from processing.savetoExcel_personal import prepare_workbook
import json

def kb(data, forcd):
    kb = InlineKeyboardMarkup(row_width=2)
    for actions in data:
        quantity = data[actions]
        d = InlineKeyboardButton(text=f"{actions} ({quantity})",
                                 callback_data=personal_callback.new(personal_action=f"{actions}",
                                                                     zone=forcd)
                                 )
        kb.insert(d)
    return kb



def get_empty_values(data):
    data['defence'] = get_zone_actions()
    data['middle'] = get_zone_actions()
    data['atack'] = get_zone_actions()
    data['shoots'] = get_shoots_actions()
    data['other'] = get_other_actions()
    print('function created empty dicts')

def get_results_value(data,half):
    data[half] = {}
    data[half]['defence'] = data['defence']
    data[half]['middle'] = data['middle']
    data[half]['atack'] = data['atack']
    data[half]['shoots'] = data['shoots']
    data[half]['other'] = data['other']


# @dp.message_handler(state=PersonalStatisticStates.Zero_state)
# async def naming(message: types.Message, state: FSMContext):
#     print(1111111)
#     async with state.proxy() as data:
#         data['name'] = message.text
#     await message.answer('имя сохранено!')
#     await PersonalStatisticStates.First_state.set()



@dp.callback_query_handler(personal_callback.filter(),
                           state=[PersonalStatisticStates.First_state,PersonalStatisticStates.Second_state])
async def personal_test(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    print(callback_data)
    whatzone = callback_data['zone']
    whataction = callback_data['personal_action']
    async with state.proxy() as data:
        data[whatzone][whataction] += 1
    await call.message.edit_reply_markup(reply_markup=kb(data[whatzone], whatzone))


@dp.message_handler(text="Второй", state=PersonalStatisticStates.First_state)
async def start_second_half(message: types.Message, state: FSMContext):
    await message.answer("Вы закончили первый тайм и начали второй!!!")
    async with state.proxy() as data:
        get_results_value(data, 'first half')
        get_empty_values(data)
        for zone in datas.ZONES:
            await message.answer(f"{zone}-2 тайм", reply_markup=kb(data[zone], zone))
    await PersonalStatisticStates.Second_state.set()


@dp.message_handler(text="Готово", state=PersonalStatisticStates.Second_state)
async def finishing(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        first_half_result = data['first half']
        get_results_value(data, 'second half')
        second_half_result = data['second half']
        name = data['name']
    prepare_workbook(file_name=name, first_half=first_half_result, second_half=second_half_result)
    await message.answer('Готово! файл отправлен!')

    total_result = dict()
    total_result['first half'] = first_half_result
    total_result['second half'] = second_half_result
    with open(f'excel complete personal/{name}.json', 'w') as js:
        json.dump(total_result, js)

    await dp.bot.send_document(chat_id=admin, document=open(f"./excel complete personal/{name}.xls", "rb"))
    await state.finish()

@dp.message_handler(state=PersonalStatisticStates.Zero_state)
async def personal_stat_start(message: types.Message, state: FSMContext):
    print(2222)
    await message.answer('Ниже 3 клавиатуры (разбиры по зонам) для подсчета первого тайма')
    async with state.proxy() as data:
        data['name'] = message.text
        get_empty_values(data)
        data['first half'] = {}
        for zones in datas.ZONES:
            print(type(data[zones]))
            print(zones)
            await message.answer(f"{zones}", reply_markup=kb(data[zones], zones))
    await PersonalStatisticStates.First_state.set()
