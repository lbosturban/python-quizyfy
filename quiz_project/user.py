#!/usr/bin/env python3
"""
File:				user.py
Author:				Laurent BOST URBAN
Creation Date:		2026-10-23 11:46:06
Email:				bostur_l@etna-alternance.net
Description:		quizify user
Last update Date:	2026-10-24 12:17:40 by bostur_l
"""

__author__ = "bostur_l"

import utils

import json
import datetime


class User(utils.Config):
    def __init__(self, name: str, category: str, score: int, quest_numb: int):
        super().__init__()
        self.name = name
        self.category = category
        self.score = score
        self.quest_numb = quest_numb
        self.percent_score = self.score / self.quest_numb

    def update_score(self):
        user_data_dict_str: str
        user_data_dict: dict
        with open(self.user_file_path) as fr:
            user_data_dict_str = fr.read()
        if len(user_data_dict_str) == 0:
            user_data_dict = {
                f"{self.name}": {
                    "scores":
                    [{"category": self.category,
                      "score": f"{self.score}/{self.quest_numb}",
                      "score%": self.percent_score, "date":
                      datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]
                }
            }
        else:
            user_data_dict = json.loads(user_data_dict_str)
            user_data_scores = user_data_dict.get(self.name, None)
            if user_data_scores is None:
                user_data_scores = {
                    "scores":
                    [{"category": self.category,
                      "score": f"{self.score}/{self.quest_numb}",
                      "score%": self.percent_score, "date":
                      datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]
                }
                user_data_dict[self.name] = user_data_scores
            else:
                user_data_score = user_data_dict[self.name]
                user_data_score["scores"].append({
                    "category": self.category,
                    "score": f"{self.score}/{self.quest_numb}",
                    "score%": self.percent_score, "date":
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            user_data_dict_str = json.dumps(user_data_dict)
            with open(self.user_file_path, "w") as fw:
                fw.write(user_data_dict_str)
