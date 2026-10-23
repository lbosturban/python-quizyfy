#!/usr/bin/env python3
"""
File:				test.py
Author:				Laurent BOST URBAN
Creation Date:		2026-10-23 13:32:25
Email:				bostur_l@etna-alternance.net
Description:		Python file.
Last update Date:	2026-10-23 15:00:31 by bostur_l
"""

__author__ = "bostur_l"

import random
import html
import json

print("sTaRtInG QUIZZZZZzzzzzzzz...:")
question_list = None
with open("./data/questions.json") as f:
    question_list = json.load(f)
for question_answer in question_list:
    print("-----------------------------------------------------------")
    category = question_answer['category']
    print(f"Category: \"{category}\"")
    difficulty = question_answer['difficulty']
    print(f"Difficulty: \"{difficulty}\"")
    is_quest_bool = question_answer["type"] == "boolean"
    type_question = "[T]rue/[F]alse" if is_quest_bool else "Multiple Choice"
    print(f"Type: {type_question}")
    question = html.unescape(question_answer['question'])
    print(f"Question: \"{question}\"\n")
    answer_list = question_answer['incorrect_answers']
    correct_answer = question_answer['correct_answer']
    answer_list.insert(0, correct_answer)
    answer_choice: str = "Choice:\n"
    answer_values: list = ["[T]rue", "[F]alse"]
    if is_quest_bool:
        answer_choice = "[T]rue or [F]alse ?\n\n (type T/t or F/f)\n: "
    else:
        answer_values = random.sample(answer_list, len(answer_list))
        answer_choice_list = list(enumerate(answer_values))
        for answer_choice_elem in answer_choice_list:
            answer_choice += f"{answer_choice_elem[0] + 1}: \
'{answer_choice_elem[1]}'\n"
        answer_choice = f"{answer_choice}\n \
(type the number, 1 or 2 or 3 ...,  of the answer chosen)\n: "
    user_answer = input(answer_choice)
    if is_quest_bool:
        if correct_answer.lower().startswith(user_answer.lower()):
            print(f"\nCORRECT: the answer is '{correct_answer}'!")
        else:
            print(f"\n_WRONG_: the answer was '{correct_answer}'!")
    else:
        if correct_answer == answer_list[int(user_answer) - 1]:
            print(f"\nCORRECT: the answer is '{correct_answer}'!")
        else:
            print(f"\n_WRONG_: the answer was '{correct_answer}'!")
print("-----------------------------------------------------------")
print("Quizz finished.\n Bye o/")
