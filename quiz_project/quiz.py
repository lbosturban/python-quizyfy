#!/usr/bin/env python3
"""
File:				quiz.py
Author:				Laurent BOST URBAN
Creation Date:		2026-10-23 11:45:59
Email:				bostur_l@etna-alternance.net
Description:		quizify quizz
Last update Date:	2026-10-24 12:28:32 by bostur_l
"""

__author__ = "bostur_l"

import utils
import user

import random
import html
import json
import requests


class Game(utils.Config):
    def __init__(self):
        super().__init__()
        self.name = "anonymous"
        self.score = 0
        self.quest_numb = 0
        self.percent_score = 0.0
        self.categories: dict = None
        self.cfg: dict = None
        with open(self.open_trivia_conf_path) as cr:
            self.cfg = json.load(cr)

    def print_header(self, menu_type: str):
        print(f"_____---------'   {menu_type} MENU   '---------_____\n")
        print(f"\tWelcome '{self.name}'\n")

    def play(self):
        print("BEGIN: _~QUIZIFY~_")
        print("sTaRtInG QUIZZZZZzzzzzzzz...:")
        self.score = 0
        question_list = None
        with open(self.curr_quest_set_path) as f:
            question_list = json.load(f)
        self.quest_numb = len(question_list)
        for question_answer in question_list:
            print("-----------------------------------------\
-------------------")
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

    def get_category_name(self) -> str:
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
                            return cat_name

    def config(self):
        command = 0
        while command >= 0:
            print(f"loop starts with command = {command}")
            utils.game_clear()
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
                    cat_name = self.get_category_name()
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
                    with open(self.open_trivia_conf_path, "w") as dw:
                        dw.write(config_json)
                    resp_quests = self.request_trivia_json(2)
                    if resp_quests is not None:
                        if resp_quests["response_code"] == 0:
                            questions_str = json.dumps(resp_quests["results"])
                            with open(self.curr_quest_set_path, "w") as qw:
                                qw.write(questions_str)
                    break
                case _:
                    break
            command = int(command)

    def start(self):
        utils.game_clear()
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
                    utils.game_clear()
                    self.play()
                case "2":
                    print("High Scores")
                case "3":
                    self.config()
                case "4":
                    break
            input("Press enter to return to the Main Menu.\n")
            utils.game_clear()
            print("BEGIN: _~QUIZIFY~_")
        print("-- \nBye o/")
        print("_END_: _~QUIZIFY~_")

    def manage_score(self):
        category_score = self.get_category_name()
        cat_num = self.cfg['cat']
        if cat_num == "":
            cat_num = 0
        else:
            cat_num = int(cat_num)
        category_score = f"{category_score} ({cat_num})"
        usr = user.User(self.name, category_score, self.score, self.quest_numb)
        usr.update_score()
