from pprint import pprint
from typing import NamedTuple

times = ("First half", "Second half")
teams = ("Team one", "Team two")



class Halfs(NamedTuple):
    first : int
    second : int


c = Halfs(8,4)
for i in c.a
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


def get_dict_of_match_info(times, actions, teams=None) -> dict:
    activities = {action: 0 for action in actions}
    return {half: {team: activities for team in teams} for half in times}

def get_dict_of_team_analytic(times: tuple, actions: tuple) -> dict:
    activities = {action: 0 for action in actions}
    return {half: activities for half in times}



pprint(get_dict_of_actions(times, team_analytic))
