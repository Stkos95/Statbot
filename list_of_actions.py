from pprint import pprint
from typing import NamedTuple
from dataclasses import dataclass
times = ("First half", "Second half")
teams = ("Team one", "Team two")


class Times(NamedTuple):
    team_one : dict
    team_two : dict


class Halfs(NamedTuple):
    first : Times
    second : Times




# ---------------------Для послематчевого табло----------------
actions_base = ('передача✅',
                'передача❌',
                'удар✅',
                'удар❌',
                'Обводка✅',
                "Обводка❌",
                "Фолы",
                "Угловые",
                "ЖК",
                "КК")
# ----------------------------------Для командной статистики-------------------
team_analytic = ('передача✅',
                 'передача❌',
                 'Прием мяча✅',
                 'Прием мяча❌',
                 'удар✅',
                 'удар❌',
                 'Обводка✅',
                 'Обводка❌',
                 'ЖК',
                 'КК',
                 '🛡Перехват✅',
                 '🛡Перехват❌',
                 '🛡Отбор✅',
                 '🛡Отбор❌',
                 'Угловые',
                 'Голевые моменты',
                 'Штрафные удары',
                 'Подборы',
                 'Потери')

def act():
    return {action: 0 for action in actions_base}

def get_actions_for_counting():
    return Halfs(first=Times(team_one=act(), team_two=act()),second=(Times(team_one=act(),team_two=act())))


def get_dict_of_match_info(times, actions, teams=None) -> dict:
    return {half: {team: {action: 0 for action in actions} for team in teams} for half in times}

def get_dict_of_team_analytic(times: tuple, actions: tuple) -> dict:
    return {half: {action: 0 for action in actions} for half in times}


