#!/usr/bin/env python3
"""
File:				test.py
Author:				Laurent BOST URBAN
Creation Date:		2026-10-23 13:32:25
Email:				bostur_l@etna-alternance.net
Description:		Python file.
Last update Date:	2026-10-23 18:37:21 by bostur_l
"""

__author__ = "bostur_l"

import datetime
import random
import html
import json

from subprocess import call
from sys import platform


class Game:
    def __init__(self):
        self.name = "anonymous"
        self.score = 0
        self.quest_numb = 0
        self.percent_score = 0.0

    def clear():
        if platform not in ('win32', 'cygwin'):
            command = 'clear'
        else:
            command = 'cls'
        call(command, shell=True)

    def play(self):
        print("BEGIN: _~QUIZIFY~_")
        print("sTaRtInG QUIZZZZZzzzzzzzz...:")
        self.score = 0
        question_list = None
        with open("./data/questions.json") as f:
            question_list = json.load(f)
        self.quest_numb = len(question_list)
        for question_answer in question_list:
            print("---------------------------------------------------------")
            category = html.unescape(question_answer['category'])
            print(f"Category: \"{category}\"")
            difficulty = question_answer['difficulty']
            print(f"Difficulty: _{difficulty}_")
            is_quest_bool = question_answer["type"] == "boolean"
            type_question: str
            if is_quest_bool:
                type_question = "[T]rue/[F]alse"
            else:
                type_question = "Multiple Choice"
            print(f"Type: {type_question}")
            question = html.unescape(question_answer['question'])
            print(f"Question:\n - \"{question}\"\n")
            answer_list = question_answer['incorrect_answers']
            correct_answer = question_answer['correct_answer']
            answer_list.insert(0, correct_answer)
            answer_choice: str = "Choice:\n"
            answer_values: list = ["[T]rue", "[F]alse"]
            if is_quest_bool:
                answer_choice = "[T]rue or [F]alse ?\n\
\n (type T/t or F/f then Enter)\n: "
            else:
                answer_values = random.sample(answer_list, len(answer_list))
                answer_choice_list = list(enumerate(answer_values))
                for answer_choice_elem in answer_choice_list:
                    answer_choice += f"{answer_choice_elem[0] + 1}: \
'{answer_choice_elem[1]}'\n"
                answer_choice = f"{answer_choice}\n \
(type the number, 1 or 2 or 3 ...,  of the answer chosen, then Enter)\n: "
            user_answer = input(answer_choice)
            if is_quest_bool:
                if correct_answer.lower().startswith(user_answer.lower()):
                    print(f"\nCORRECT: the answer is '{correct_answer}'!")
                    self.score += 1
                else:
                    print(f"\n_WRONG_: the answer was '{correct_answer}'!")
            else:
                if correct_answer == answer_values[int(user_answer) - 1]:
                    print(f"\nCORRECT: the answer is '{correct_answer}'!")
                    self.score += 1
                else:
                    print(f"\n_WRONG_: the answer was '{correct_answer}'!")
            print("---------------------------------------------------------")
            print("Quizz finished.\n")
            self.percent_score =\
                float(f"{self.score * 100 / self.quest_numb:.2f}")
            print(f"{self.name}:\n\
Your score is {self.score}/{self.quest_numb}\n \
(percent={self.percent_score}).")
            self.manage_score()

    def start(self):
        Game.clear()
        print("BEGIN: _~QUIZIFY~_")
        name = input("Please enter your name\n (no name is 'anonymous')\n:")
        if name != "":
            self.name = name
        command = 0
        while command != "3":
            print("_____---------'   MENU   '---------_____\n")
            print(f"\tWelcome '{self.name}'\n")
            print("1. Play")
            print("2. High Scores")
            print("3. Quit\n\n")
            command = input(" (press 1 or 2 or 3 then Enter)\n: ")
            if command == "1":
                Game.clear()
                self.play()
            elif command == "2":
                print("High Scores")
            elif command == "3":
                break
            input("Press enter to return to the Menu.\n")
            Game.clear()
            print("BEGIN: _~QUIZIFY~_")
        print("-- \nBye o/")
        print("_END_: _~QUIZIFY~_")

    def manage_score(self):
        user_data_dict_str: str
        user_data_dict: dict
        with open("./data/utilisateurs.json") as fr:
            user_data_dict_str = fr.read()
        if len(user_data_dict_str) == 0:
            user_data_dict = {
                f"{self.name}":
                {
                    "scores":
                    [{"score": f"{self.score}/{self.quest_numb}",
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
                    [{"score": f"{self.score}/{self.quest_numb}",
                      "score%": self.percent_score, "date":
                      datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]
                }
                user_data_dict[self.name] = user_data_scores
            else:
                user_data_score = user_data_dict[self.name]
                user_data_score["scores"].append({
                    "score": f"{self.score}/{self.quest_numb}",
                    "score%": self.percent_score, "date":
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            user_data_dict_str = json.dumps(user_data_dict)
            with open("./data/utilisateurs.json", "w") as fw:
                fw.write(user_data_dict_str)


game = Game()
game.start()
