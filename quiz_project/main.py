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

import fcntl
from pathlib import Path

from quiz import Game


def main() -> None:
    """ main game entry """
    script_dir = Path(__file__).resolve().parent
    if Path.cwd().resolve() != script_dir:
        print(f"Run this program from its folder: {script_dir}")
        return

    lock_path = Path(__file__).resolve().parent / ".quizify.lock"

    with open(lock_path, "w", encoding="utf-8") as lock_file:
        try:
            fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("Quizify is already running.")
            return
        
    try:
        game = Game()
        game.start()
    except EOFError:
        print("=Exiting as EOF=")
    except Exception as error:
        print(f"Quizify stopped with an error: {error}")


if __name__ == "__main__":
    main()
