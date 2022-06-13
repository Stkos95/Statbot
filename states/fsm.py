from aiogram.dispatcher.filters.state import StatesGroup, State


class SummaryStates(StatesGroup):
    First_state = State()
    Second_state = State()

class PersonalStatisticStates(StatesGroup):
    First_state = State()
    Second_state = State()