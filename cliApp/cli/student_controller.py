from typing import Optional
from .ui import ask, say, C_SKY, C_GREEN, C_YELLOW, C_RED, SUBMENU_STEP
from ..core.validation import valid_email, valid_password, email_to_name
from ..core.models import Student
from ..core.db import Database
from ..core.util import gen_student_id
from . import enrolment_controller as enr

def student_register(depth: int) -> None:
    say(depth, "Student Sign Up", C_GREEN)
    while True:
        email = ask(depth, "Email: ")
        password = ask(depth, "Password: ")
        if not (valid_email(email) and valid_password(password)):
            say(depth, "Incorrect email or password format", C_RED)
            continue
        say(depth, "email and password formats acceptable", C_YELLOW)

        students = Database.load_students()
        if any(s.email.lower() == email.lower() for s in students):
            fullname = email_to_name(email)
            say(depth, f"Student {fullname} already exists", C_RED)
            return

        name = ask(depth, "Name: ")
        fullname = email_to_name(email)
        say(depth, f"Enrolling student {fullname}", C_YELLOW)

        new_id = gen_student_id([s.id for s in students])
        new_student = Student(new_id, name, email, password, [])
        students.append(new_student)
        Database.save_students(students)
        return

def student_login(depth: int) -> Optional[Student]:
    say(depth, "Student Sign In", C_GREEN)
    while True:
        email = ask(depth, "Email: ")
        password = ask(depth, "Password: ")
        if not (valid_email(email) and valid_password(password)):
            say(depth, "Incorrect email or password format", C_RED)
            continue
        say(depth, "email and password formats acceptable", C_YELLOW)
        students = Database.load_students()
        stu = next((s for s in students if s.email.lower() == email.lower()), None)
        if stu is None:
            say(depth, "Student does not exist", C_RED)
            return None
        if stu.password != password:
            say(depth, "Password incorrect", C_RED)
            return None
        return stu

def student_change_password(depth: int, stu: Student) -> None:
    say(depth, "Updating Password", C_YELLOW)
    while True:
        new_pw = ask(depth, "New Password: ")
        if not valid_password(new_pw):
            say(depth, "Password format does not match", C_RED)
            continue
        break
    while True:
        conf = ask(depth, "Confirm Password: ")
        if conf != new_pw:
            say(depth, "Password does not match - try again", C_RED)
            continue
        students = Database.load_students()
        for s in students:
            if s.id == stu.id:
                s.password = new_pw
                Database.save_students(students)
                stu.password = new_pw
                return

def student_course_menu(depth: int, stu: Student) -> None:
    while True:
        cmd = ask(depth, "Student Course Menu (c/e/r/s/x): ", C_SKY).lower()
        if cmd == "c":
            student_change_password(depth, stu)          # same depth
        elif cmd == "e":
            enr.enrol_subject(depth, stu)                # same depth
        elif cmd == "r":
            enr.remove_subject(depth, stu)               # same depth
        elif cmd == "s":
            enr.show_subjects(depth, stu)                # same depth
        elif cmd == "x":
            return
        else:
            say(depth, "Unknown command", C_RED)

def student_menu(depth: int) -> None:
    while True:
        cmd = ask(depth, "Student System (l/r/x): ", C_SKY).lower()
        if cmd == "r":
            student_register(depth)                      # same depth
        elif cmd == "l":
            stu = student_login(depth)                   # same depth
            if stu:
                student_course_menu(depth + SUBMENU_STEP, stu)  # submenu jump
        elif cmd == "x":
            return
        else:
            say(depth, "Unknown command", C_RED)
