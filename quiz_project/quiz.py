#!/usr/bin/env python3
"""
File:			quiz.py
Author:			Laurent BOST URBAN
Creation Date:		2026-10-23 11:45:59
Email:			bostur_l@etna-alternance.net
Description:		quizify quizz
Last update Date:	2026-10-24 12:44:29 by bostur_l
"""

__author__ = "bostur_l"


import utils
import user
import csv
import random
import html
import json
import requests


class Game(utils.Config):
    """ main game class for the quizz """
    def __init__(self):
        """ game ctor """
        super().__init__()
        self.name = "anonymous"
        self.score = 0
        self.quest_numb = 5
        self.percent_score = 0.0
        self.categories: dict = None
        self.cfg: dict = None
        with open(self.open_trivia_conf_path) as cr:
            self.cfg = json.load(cr)

    # TODO: more sub method to simplify code """
    def print_header(self, menu_type: str):
        """ just prints the header """
        print(f"_____---------'   {menu_type} MENU   '---------_____\n")
        print(f"\tWelcome '{self.name}'\n")

    @staticmethod
    def read_choice_true_false(prompt: str) -> str:
        choice = 0
        valid_choices: set[str] = {"t", "true", "f", "false"}
        while type(choice) is int:
            try:
                choice = input(prompt).strip().lower()
                if choice in valid_choices:
                    return choice[0]
                else:
                    choice = 0
            except ValueError:
                choice = 0
            finally:
                if type(choice) is int and choice == 0:
                    print(f"Enter one of (case insensitive): \
{', '.join(valid_choices)}\n")

    @staticmethod
    def read_choice_set_int(prompt: str, valid_choices: set[int]) -> int:
        choice = ''
        while type(choice) is str:
            try:
                choice = int(input(prompt))
                if choice in valid_choices:
                    return choice
                else:
                    choice = ''
            except ValueError:
                choice = ''
            finally:
                if type(choice) is str and choice == '':
                    print(f"Enter one of: \
{', '.join(map(str, sorted(valid_choices)))}\n")

    @staticmethod
    def read_choice_min_max(prompt: str, min_val: int, max_val: int) -> int:
        choice = ''
        while type(choice) is str:
            try:
                choice = int(input(prompt))
                if min_val <= choice and choice <= max_val:
                    return choice
                else:
                    choice = ''
            except ValueError:
                choice = ''
            finally:
                if type(choice) is str and choice == '':
                    print(f"Enter a value between {min_val}\
(included) and {max_val} (included)\n")
                
    def play(self):
        """ main game loop with questions """
        print("BEGIN: _~QUIZIFY~_")
        print("sTaRtInG QUIZZZZZzzzzzzzz...:")
        self.score = 0
        question_list = None
        with open(self.curr_quest_set_path) as f:
            question_list = json.load(f)
        self.quest_numb = len(question_list)
        if self.quest_numb == 0:
            raise ValueError("There's no way I'd do a quizz with 0 questions!")
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
            answer_list = [html.unescape(s) for s in question_answer['incorrect_answers']]
            correct_answer = html.unescape(question_answer['correct_answer'])
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
            if is_quest_bool:
                user_answer = Game.read_choice_true_false(answer_choice)
                if correct_answer.lower().startswith(user_answer):
                    print(f"\n|\nCORRECT:\n\
the answer is '{correct_answer}'!\n|\n")
                    self.score += 1
                else:
                    print(f"\n|\n_WRONG_:\n\
the answer was '{correct_answer}'!\n|\n")
            else:
                user_answer = Game.read_choice_set_int(answer_choice,
                                                       {1, 2, 3, 4})
                if correct_answer == answer_values[user_answer - 1]:
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
        if self.name != "anonymous":
            self.manage_score()

    def _get_json(self,
                  url: str,
                  *, params: dict | None = None) -> dict | None:
        """Make a GET request and return its JSON, or None if it fails."""
        try:
            response = requests.get(url, params=params, timeout=(3.05, 10))
            response.raise_for_status()
            data = response.json()

            if not isinstance(data, dict):
                print("API error: expected a JSON object.")
                return None

            return data

        except requests.exceptions.Timeout:
            print("The trivia API request timed out. Please try again.")
        except requests.exceptions.HTTPError as error:
            print(f"The trivia API returned an HTTP error: {error}")
        except requests.exceptions.RequestException as error:
            print(f"Could not connect to the trivia API: {error}")
        except ValueError:
            print("The trivia API returned invalid JSON.")

        return None

    def request_trivia_json(self, req_type: int):
        """Fetch trivia categories or questions."""
        categories_url = "https://opentdb.com/api_category.php"
        
        match req_type:
            case 0:
                if self.categories is None:
                    self.categories = self._get_json(categories_url)
            case 1:
                cat: dict
                if self.categories is None:
                    self.categories = self._get_json(categories_url)
                    if self.categories is None:
                        return None
                cat = self.categories
                cat_choice_list = list(enumerate(cat["trivia_categories"]))
                cat_choice_txt: str = "\nChoice:\n0. Any Category\n"
                i = 0
                for cat_choice in cat_choice_list:
                    num = cat_choice[0] + 1
                    obj = cat_choice[1]
                    name = obj.get('name')
                    cat_choice_txt += f"{num}. {name}\n"
                    i += 1
                cat_choice_txt = f"{cat_choice_txt}\n\
 (type the number, 1 or 2 or 3 ...,  of the answer chosen, then Enter)\n: "
                cat_user_choice = Game.read_choice_min_max(cat_choice_txt,
                                                           0, i)
                if cat_user_choice == 0:
                    self.cfg['cat'] = ""
                else:
                    selected_cat = cat_choice_list[cat_user_choice - 1][1]
                    id_cat = selected_cat.get('id')
                    self.cfg['cat'] = str(id_cat)
                return self.cfg
            case 2:
                params = {"amount": self.cfg["quest"]}
                if self.cfg.get("cat"):
                    params["category"] = self.cfg["cat"]
                if self.cfg.get("diff"):
                    params["difficulty"] = self.cfg["diff"]
                if self.cfg.get("type"):
                    params["type"] = self.cfg["type"]
                response_data = self._get_json("https://opentdb.com/api.php",
                                               params=params)
                if response_data is None:
                    return None
                if response_data.get("response_code") != 0:
                    print("The trivia API could not provide questions \
for this configuration. Try different configuration options.")
                    return None
                else:
                    return response_data
            case _:
                return None
        return None

    def get_category_name(self) -> str:
        """ quick method to translate cat number into name """
        cat_name = "All Categories"
        cat_val = self.cfg.get('cat', None)
        if cat_val is None or cat_val == "":
            cat_val = 0
        else:
            cat_val = int(cat_val)
            if cat_val > 0:
                if self.categories is None:
                    self.request_trivia_json(0)
                    if self.categories is None:
                        return cat_name
                    for cat_obj in self.categories['trivia_categories']:
                        if cat_val == cat_obj['id']:
                            cat_name = cat_obj['name']
                            return cat_name

    def config(self):
        """ manage opendb configuration for download auestions """
        command = 0
        while command >= 0:
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
            command = Game.read_choice_set_int(" (press 1 or 2 or\
... then Enter)\n:",
                                          {0, 1, 2, 3, 4, 6, 8})
            match command:
                case 0:
                    break
                case 1:
                    updtd_cfg = self.request_trivia_json(1)
                    if updtd_cfg is not None:
                        self.cfg = updtd_cfg
                case 2:
                    diff_txt = "Choice:\n\
0. Any Difficulty\n1. Easy\n2. Medium\n3. Hard\n \
 (type the number, 0 or 1 or 2 ...,  of the answer chosen, then Enter)\n: "
                    diff = Game.read_choice_set_int(diff_txt, {0, 1, 2, 3})
                    if diff == 0:
                        self.cfg["diff"] = ""
                    else:
                        self.cfg["diff"] = utils.Difficulty(diff).name.lower()
                case 3:
                    qtype_txt = "Choice:\n\
0. Any Type\n1. Multiple Choice\n2. [T]rue/[F]alse\n \
 (type the number, 0 or 1 or 2, of the answer chosen, then Enter)\n: "
                    qtype = Game.read_choice_set_int(qtype_txt, {0, 1, 2})
                    if qtype == 0:
                        self.cfg['type'] = ""
                    else:
                        self.cfg['type'] = utils.Qtype(int(qtype)).name.lower()
                case 4:
                    nb_txt = "\nType a number beetwen 5 and 50:\n \
(then Enter)\n: "
                    nb = Game.read_choice_min_max(nb_txt, 5, 50)
                    self.cfg["quest"] = nb
                case 6:
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
                case 8:
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
            command = 0

    def start(self):
        """ launch the game """
        utils.game_clear()
        print("BEGIN: _~QUIZIFY~_")
        name = input("Please enter your name\n (no name is 'anonymous' with no score saving)\n:")
        if name != "":
            self.name = name
        command = 0
        while command != "4":
            self.print_header("MAIN")
            print("1. Play")
            print("2. High Scores")
            print("3. Hall of Fame")
            print("4. Configure Quizz")
            print("5. Quit\n\n")
            command_txt = " (press 1 or 2 or 3 ... then Enter)\n: "
            command = Game.read_choice_set_int(command_txt, {1, 2, 3, 4, 5})
            match command:
                case 1:
                    utils.game_clear()
                    self.play()
                case 2:
                    self.display_high_scores()
                case 3:
                    self.display_hall_of_fame()
                case 4:
                    self.config()
                case 5:
                    break
            input("Press enter to return to the Main Menu.\n")
            utils.game_clear()
            print("BEGIN: _~QUIZIFY~_")
        print("-- \nBye o/")
        print("_END_: _~QUIZIFY~_")

    def manage_score(self):
        """ manage user score and saves it """
        category_score = self.get_category_name()
        cat_num = self.cfg['cat']
        if cat_num == "":
            cat_num = 0
        else:
            cat_num = int(cat_num)
        category_score = f"{category_score} ({cat_num})"
        usr = user.User(self.name, category_score,
                        self.score, self.quest_numb)
        usr.update_score()

    @staticmethod
    def _score_sort_key(entry: dict) -> tuple:
        """Sort scores by correct answers, then by score denominator."""
        return (entry["correct"], entry["total"])


    def display_high_scores(self):
        """Display and export the top 10 users overall and per category."""
        try:
            with open(self.user_file_path, encoding="utf-8") as score_file:
                users_data = json.load(score_file)
        except FileNotFoundError:
            print("No saved scores yet.")
            return
        except (json.JSONDecodeError, OSError) as error:
            print(f"Could not read saved scores: {error}")
            return

        if not isinstance(users_data, dict) or not users_data:
            print("No saved scores yet.")
            return

        # Convert the stored score strings, such as "8/10", to numbers.
        all_entries = []
        for username, user_data in users_data.items():
            scores = user_data.get("scores",
                                   []) if isinstance(user_data, dict) else []

            for score in scores:
                if not isinstance(score, dict):
                    continue

                try:
                    correct_text, total_text = str(score["score"]).split("/",
                                                                         1)
                    correct = int(correct_text)
                    total = int(total_text)
                    if total <= 0 or correct < 0:
                        continue
                except (KeyError, TypeError, ValueError):
                    continue

                all_entries.append({
                    "username": str(username),
                    "category": str(score.get("category", "Unknown")),
                    "correct": correct,
                    "total": total,
                    "date": str(score.get("date", "")),
                })

        if not all_entries:
            print("No valid saved scores found.")
            return

        categories = sorted({entry["category"] for entry in all_entries})

        # “Overall” combines all categories. Each other board includes only
        # scores saved for that category.
        boards = [("Overall (All Categories)", all_entries)]
        boards.extend(
            (category, [
                entry for entry in all_entries
                if entry["category"] == category
            ])
            for category in categories)

        csv_rows = []

        for board_name, entries in boards:
            # Group each user's attempts, then select their best attempt.
            user_entries = {}
            for entry in entries:
                user_entries.setdefault(entry["username"], []).append(entry)

            ranked_users = []
            for username, scores in user_entries.items():
                ordered_scores = sorted(
                    scores,
                    key=self._score_sort_key,
                    reverse=True)
                ranked_users.append((username, ordered_scores))

            ranked_users.sort(
                key=lambda item: (
                    -item[1][0]["correct"],
                    item[0].casefold()))
            ranked_users = ranked_users[:10]

            print(f"\n=== {board_name} High Scores ===")
            if not ranked_users:
                print("No scores for this category.")
                continue

            for rank, (username, scores) in enumerate(ranked_users, start=1):
                best_score = scores[0]
                history = scores[:5]
                history_text = ", ".join(
                    f'{score["correct"]}/{score["total"]}'
                    for score in history)

                print(
                    f"{rank}. {username} — "
                    f'{best_score["correct"]}/{best_score["total"]} '
                    f"(best; top scores: {history_text})")

                csv_rows.append({
                    "category": board_name,
                    "rank": rank,
                    "username": username,
                    "best_score": (
                        f'{best_score["correct"]}/{best_score["total"]}'),
                    "top_scores": history_text})

            input("\nPress Enter to continue to the next leaderboard...")

        try:
            with open(self.user_score_board,
                      "w", newline="", encoding="utf-8") as csv_file:
                fieldnames = [
                    "category",
                    "rank",
                    "username",
                    "best_score",
                    "top_scores",
                ]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(csv_rows)

            print(f"\nLeaderboard saved to {self.user_score_board}")
        except OSError as error:
            print(f"Could not save the leaderboard CSV: {error}")

    def display_hall_of_fame(self):
        """Display saved user score data, ordered by username."""
        try:
            with open(self.user_file_path, encoding="utf-8") as user_file:
                users_data = json.load(user_file)
        except FileNotFoundError:
            print("No Hall of Fame data found yet.")
            return
        except json.JSONDecodeError:
            print("The Hall of Fame file is empty or contains invalid JSON.")
            return
        except OSError as error:
            print(f"Could not read the Hall of Fame file: {error}")
            return

        if not isinstance(users_data, dict) or not users_data:
            print("The Hall of Fame is empty.")
            return

        print("\n_____---------'   HALL OF FAME   '---------_____\n")

        for username in sorted(users_data, key=str.casefold):
            user_data = users_data[username]
            scores = user_data.get("scores",
                                   []) if isinstance(user_data, dict) else []

            print(f"Player:\n{username}")
            print("-" * (len(username) or 1))

            if not scores:
                print("  No saved scores.\n")
                continue

            # Group this user's scores by category
            scores_by_category = {}
            for score in scores:
                if isinstance(score, dict):
                    category = score.get("category", "Unknown")
                    scores_by_category.setdefault(category, []).append(score)

            for category in sorted(scores_by_category, key=str.casefold):
                print(f"\n  {category}")

                for score in scores_by_category[category]:
                    percent = score.get("score%", "Unknown")
                    if isinstance(percent, (int, float)):
                        # Stored percentages are fractions.
                        percent = percent * 100 if percent <= 1 else percent
                        percent = f"{percent:.2f}%"

                    print(f"    Score Percent:       \
{percent}")
                    print(f"    Actual Score:        \
{score.get('score', 'Unknown')}")
                    print(f"    Questions Answered:  \
{score.get('#quest', 'Unknown')}")
                    print(f"    Date:                \
{score.get('date', 'Unknown')}")

                    # Show any additional score fields.
                    displayed_fields = {
                        "category", "score%", "score", "#quest", "date"
                    }
                    for field, value in score.items():
                        if field not in displayed_fields:
                            print(f"    {field}: {value}")
                    print()
