from aiogram.dispatcher.filters.state import StatesGroup, State


class SummaryStates(StatesGroup):
    Zero_state = State()
    First_state = State()
    Second_state = State()


class TeamAnalytic(StatesGroup):
    Zero_state = State()
    First_state = State()
    Second_state = State()

class PersonalStatisticStates(StatesGroup):
    Zero_state = State()
    First_state = State()
    Second_state = State()