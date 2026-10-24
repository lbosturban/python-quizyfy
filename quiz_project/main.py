#!/usr/bin/env python3
"""
File:				main.py
Author:				Laurent BOST URBAN
Creation Date:		2026-10-23 11:45:45
Email:				bostur_l@etna-alternance.net
Description:		quizify main
Last update Date:	2026-10-24 11:45:14 by bostur_l
"""

__author__ = "bostur_l"

from quizz import Game


def main() -> None:
    try:
        game = Game()
        game.start()
    except Exception as error:
        print(error)
