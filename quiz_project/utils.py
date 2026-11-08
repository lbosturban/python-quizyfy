#!/usr/bin/env python3
"""
File:			utils.py
Author:			Laurent BOST URBAN
Creation Date:		2026-10-23 11:46:11
Email:			bostur_l@etna-alternance.net
Description:		quizify utils
Last update Date:	2026-10-24 12:35:02 by bostur_l
"""

__author__ = "bostur_l"


from enum import Enum
from subprocess import call
from sys import platform


class Config:
    """ global config to avoid global values"""
    def __init__(self):
        """ config ctor """
        self.user_file_path = "./data/utilisateurs.json"
        self.open_trivia_conf_path = "./data/opentdb.json"
        self.curr_quest_set_path = "./data/questions.json"
        self.default_categories_path = "./data/categories.json"
        self.user_score_board = "./data/scoreboard.csv"


class Difficulty(Enum):
    """ enum to represent question difficulty """
    ANY = 0
    EASY = 1
    MEDIUM = 2
    HARD = 3


class Qtype(Enum):
    """ enum to represent question type """
    ANY = 0
    MULTIPLE = 1
    BOOLEAN = 2


def game_clear():
    """ method to universally clear the screen """
    if platform not in ('win32', 'cygwin'):
        command = 'clear'
    else:
        command = 'cls'
    call(command, shell=True)
