import random
from .ui import say, ask, C_YELLOW, C_RED
from ..core.models import Student, Subject, grade_from_mark
from ..core.db import Database
from ..core.util import gen_subject_id

def enrol_subject(depth: int, stu: Student) -> None:
    if not stu.can_enrol_more():
        say(depth, "Students are allowed to enrol in 4 subjects only", C_RED)
        return

    sid = gen_subject_id([s.id for s in stu.subjects])
    mark = random.randint(25, 100)
    grd  = grade_from_mark(mark)

    say(depth, f"Enrolling in Subject-{sid}", C_YELLOW)

    students = Database.load_students()
    for s in students:
        if s.id == stu.id:
            s.subjects.append(Subject(sid, mark, grd))
            Database.save_students(students)
            stu.subjects.append(Subject(sid, mark, grd))  # mirror in-memory
            break

    say(depth, f"You are now enrolled in {len(stu.subjects)} out of 4 subjects", C_YELLOW)

def show_subjects(depth: int, stu: Student) -> None:
    for sub in stu.subjects:
        say(depth, f"[Subject::{sub.id} -- mark = {sub.mark} -- grade = {sub.grade}]")

def remove_subject(depth: int, stu: Student) -> None:
    sid = ask(depth, "Remove Subject by ID: ")
    if not any(s.id == sid for s in stu.subjects):
        say(depth, "No subject found", C_RED)
        return

    stu.subjects = [x for x in stu.subjects if x.id != sid]

    students = Database.load_students()
    for s in students:
        if s.id == stu.id:
            s.subjects = stu.subjects
            break
    Database.save_students(students)

    say(depth, f"Droping Subject-{sid}", C_YELLOW)
    say(depth, f"You are now enrolled in {len(stu.subjects)} out of 4 subjects", C_YELLOW)
