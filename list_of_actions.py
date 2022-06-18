
from typing import NamedTuple
import datas


times = ("First half", "Second half")
teams = ("Team one", "Team two")

class Teams(NamedTuple):
    team_one: dict
    team_two: dict



#-------------------Summary-----------------------------
def act():
    return {action: 0 for action in datas.ACTIONS_FOR_KB}

#---------------------Personal-------------------------

def get_zone_actions():
    return {i: 0 for i in datas.ACTIONS_FOR_PERSONAL}


def get_other_actions():
    return {i: 0 for i in datas.OTHER}


def get_shoots_actions():
    return {i: 0 for i in datas.SHOOTS}

# def get_actions_for_counting():
#     return Teams(team_one=act(), team_two=act())


# def get_dict_of_match_info(times, actions, teams=None) -> dict:
#     return {half: {team: {action: 0 for action in actions} for team in teams} for half in times}
#
#
# def get_dict_of_team_analytic(times: tuple, actions: tuple) -> dict:
#     return {half: {action: 0 for action in actions} for half in times}


