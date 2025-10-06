from .ui import ask, say, C_SKY, C_YELLOW, C_RED, SUBMENU_STEP
from ..core.db import Database
from .admin_controller import admin_menu
from .student_controller import student_menu

def university_menu() -> None:
    Database.ensure_file()
    depth = 0
    while True:
        cmd = ask(depth, "University System: (A)dmin, (S)tudent, or X: ", C_SKY).lower()
        if cmd == "a":
            admin_menu(depth + SUBMENU_STEP)
        elif cmd == "s":
            student_menu(depth + SUBMENU_STEP)
        elif cmd == "x":
            say(depth, "Thank You", C_YELLOW)
            return
        else:
            say(depth, "Unknown command", C_RED)
