#!/usr/bin/env python3
"""
File:			main.py
Author:			Laurent BOST URBAN
Creation Date:		2026-10-23 11:45:45
Email:			bostur_l@etna-alternance.net
Description:		quizify main
Last update Date:	2026-10-24 12:37:03 by bostur_l
"""

__author__ = "bostur_l"

from quiz import Game


# TODO: manage lock run file main
def main() -> None:
    """ main game entry """
    try:
        game = Game()
        game.start()
    except Exception as error:
        print(error)


main()
