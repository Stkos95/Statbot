
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


