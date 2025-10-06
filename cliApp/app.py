#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .cli.university_menu import university_menu
from .cli.ui import say, C_YELLOW

if __name__ == "__main__":
    try:
        university_menu()
    except KeyboardInterrupt:
        print()
        say(0, "Thank You", C_YELLOW)