#!/usr/bin/env python3
"""
File:				test.py
Author:				Laurent BOST URBAN
Creation Date:		2026-10-23 13:32:25
Email:				bostur_l@etna-alternance.net
Description:		Python file.
Last update Date:	2026-10-24 12:19:58 by bostur_l
"""

__author__ = "bostur_l"

import datetime
import random
import html
import json
import requests

from enum import Enum
from subprocess import call
from sys import platform


class Difficulty(Enum):
    ANY = 0
    EASY = 1
    MEDIUM = 2
    HARD = 3


class Qtype(Enum):
    ANY = 0
    MULTIPLE = 1
    BOOLEAN = 2


class Game:
    def __init__(self):
        self.name = "anonymous"
        self.score = 0
        self.quest_numb = 0
        self.percent_score = 0.0
        self.categories: dict = None
        self.cfg: dict = None
        with open("./data/opentdb.json") as cr:
            self.cfg = json.load(cr)

    def clear():
        if platform not in ('win32', 'cygwin'):
            command = 'clear'
        else:
            command = 'cls'
        call(command, shell=True)

    def print_header(self, menu_type: str):
        print(f"_____---------'   {menu_type} MENU   '---------_____\n")
        print(f"\tWelcome '{self.name}'\n")

    def play(self):
        print("BEGIN: _~QUIZIFY~_")
        print("sTaRtInG QUIZZZZZzzzzzzzz...:")
        self.score = 0
        question_list = None
        with open("./data/questions.json") as f:
            question_list = json.load(f)
        self.quest_numb = len(question_list)
        for question_answer in question_list:
            print("-----------------------------------------\
--------------------")
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
                    print(f"\n|\nCORRECT:\n\
the answer is '{correct_answer}'!\n|\n")
                    self.score += 1
                else:
                    print(f"\n|\n_WRONG_:\n\
the answer was '{correct_answer}'!\n|\n")
            else:
                if correct_answer == answer_values[int(user_answer) - 1]:
                    print(f"\n|\nCORRECT:\n\
the answer is '{correct_answer}'!\n|\n")
                    self.score += 1
                else:
                    print(f"\n|\n_WRONG_:\n\
the answer was '{correct_answer}'!\n|\n")
        print("------------------------------------------------------------")
        print("Quizz finished.\n")
        self.percent_score =\
            float(f"{self.score * 100 / self.quest_numb:.2f}")
        print(f"{self.name}:\n\
Your score is {self.score}/{self.quest_numb}\n \
(percent={self.percent_score}).")
        self.manage_score()

    def request_trivia_json(self, req_type: int):
        match req_type:
            case 0:
                if self.categories is None:
                    url = "https://opentdb.com/api_category.php"
                    r = requests.get(url)
                    self.categories = json.loads(r.content)
            case 1:
                cat: dict
                if self.categories is None:
                    url = "https://opentdb.com/api_category.php"
                    r = requests.get(url)
                    self.categories = json.loads(r.content)
                cat = self.categories
                cat_choice_list = list(enumerate(cat["trivia_categories"]))
                cat_choice_text: str = "\nChoice:\n0. Any Category\n"
                for cat_choice in cat_choice_list:
                    num = cat_choice[0] + 1
                    obj = cat_choice[1]
                    name = obj.get('name')
                    cat_choice_text += f"{num}. {name}\n"
                cat_choice_text = f"{cat_choice_text}\n\
 (type the number, 1 or 2 or 3 ...,  of the answer chosen, then Enter)\n: "
                cat_user_choice = input(cat_choice_text)
                if cat_user_choice == "0":
                    self.cfg['cat'] = ""
                else:
                    cat_user_choice = int(cat_user_choice)
                    selected_cat = cat_choice_list[cat_user_choice - 1][1]
                    id_cat = selected_cat.get('id')
                    self.cfg['cat'] = str(id_cat)
                return self.cfg
            case 2:
                nb = self.cfg['quest']
                cat = self.cfg['cat']
                if cat != "":
                    cat = f"&category={cat}"
                diff = self.cfg['diff']
                if diff != "":
                    diff = f"&difficulty={diff}"
                qtype = self.cfg['type']
                if qtype != "":
                    qtype = f"&type={qtype}"
                url = f"https://opentdb.com/api.php?\
amount={nb}{cat}{diff}{qtype}"
                r = requests.get(url)
                resp = json.loads(r.content)
                if resp["response_code"] != 0:
                    print("ERROR: config")
                    return None
                else:
                    return resp
            case _:
                return None
        return None

    def config(self):
        command = 0
        while command >= 0:
            print(f"loop starts with command = {command}")
            Game.clear()
            print("BEGIN: _~QUIZIFY~_")
            self.print_header("CONFIG")
            print("0. No Change")
            print("1. Select Category")
            print("2. Select Difficulty")
            print("3. Select Type")
            print("4. Choose Number of questions")
            print("6. Display current config")
            print("8. Save Changes & Return to Main Menu\n\n")
            command = input(" (press 1 or 2 or ... then Enter)\n: ")
            match command:
                case "0":
                    break
                case "1":
                    self.cfg = self.request_trivia_json(1)
                case "2":
                    diff = input("Choice:\n\
0. Any Difficulty\n1. Easy\n2. Medium\n3. Hard\n \
 (type the number, 0 or 1 or 2 ...,  of the answer chosen, then Enter)\n: ")
                    if diff == "0":
                        self.cfg["diff"] = ""
                    else:
                        self.cfg["diff"] = Difficulty(int(diff)).name.lower()
                case "3":
                    qtype = input("Choice:\n\
0. Any Type\n1. Multiple Choice\n2. [T]rue/[F]alse\n \
 (type the number, 0 or 1 or 2, of the answer chosen, then Enter)\n: ")
                    if qtype == "0":
                        self.cfg['type'] = ""
                    else:
                        self.cfg['type'] = Qtype(int(qtype)).name.lower()
                case "4":
                    nb = input("\nType a number beetwen 10 and 50:\n \
(then Enter)\n: ")
                    self.cfg["quest"] = int(nb)
                case "6":
                    nb_quest = self.cfg['quest']
                    cat_name = "All Categories"
                    cat_val = self.cfg.get('cat', None)
                    if cat_val is None or cat_val == "":
                        cat_val = 0
                    else:
                        cat_val = int(cat_val)
                    if cat_val > 0:
                        if self.categories is None:
                            self.request_trivia_json(0)
                        for cat_obj in self.categories['trivia_categories']:
                            if cat_val == cat_obj['id']:
                                cat_name = cat_obj['name']
                                break
                    diff_name = self.cfg.get('diff', None)
                    if diff_name is None or diff_name == "":
                        diff_name = "Any Difficulty"
                    else:
                        diff_name = diff_name.capitalize()
                    qtype_name = "Any Type"
                    qtype = self.cfg.get('type', None)
                    if qtype is not None and qtype != "":
                        if qtype == "boolean":
                            qtype_name = "[T]rue/[F]alse"
                        else:
                            qtype_name = "Multiple Choice"
                    pretty_print_cfg = f"Number of Questions:\t{nb_quest}\n\
Category:\t\t{cat_name}\nDifficulty:\t\t{diff_name}\nType:\t\t\t{qtype_name}"
                    print("\n" + pretty_print_cfg + "\n\n")
                    input("Type Enter for you to enter your next choice:\n")
                case "8":
                    config_json = json.dumps(self.cfg)
                    with open("./data/opentdb.json", "w") as dw:
                        dw.write(config_json)
                    resp_quests = self.request_trivia_json(2)
                    if resp_quests is not None:
                        if resp_quests["response_code"] == 0:
                            questions_str = json.dumps(resp_quests["results"])
                            with open("./data/questions.json", "w") as qw:
                                qw.write(questions_str)
                    break
                case _:
                    break
            command = int(command)

    def start(self):
        Game.clear()
        print("BEGIN: _~QUIZIFY~_")
        name = input("Please enter your name\n (no name is 'anonymous')\n:")
        if name != "":
            self.name = name
        command = 0
        while command != "4":
            self.print_header("MAIN")
            print("1. Play")
            print("2. High Scores")
            print("3. Configure Quizz")
            print("4. Quit\n\n")
            command = input(" (press 1 or 2 or 3 then Enter)\n: ")
            match command:
                case "1":
                    Game.clear()
                    self.play()
                case "2":
                    print("High Scores")
                case "3":
                    self.config()
                case "4":
                    break
            input("Press enter to return to the Main Menu.\n")
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


try:
    game = Game()
    game.start()
except Exception as error:
    print(error)
