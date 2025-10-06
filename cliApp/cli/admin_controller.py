from .ui import ask, say, C_SKY, C_YELLOW, C_RED
from ..core.db import Database
from ..core.models import Student, grade_from_mark

def admin_clear(depth: int) -> None:
    say(depth, "Clearing students database", C_YELLOW)
    ans = ask(depth, "Are you sure you want to clear the database (Y)ES/(N)O: ", C_RED)
    if ans.strip().upper() == "Y":
        Database.clear()
        say(depth, "Clearing students database", C_YELLOW)

def admin_group_by_grade(depth: int) -> None:
    students = Database.load_students()
    # No data: print "<Nothing to Display>" with two extra indents
    if not students:
        say(depth + 2, "<Nothing to Display>")
        return

    buckets = {"N/A": [], "Z": [], "P": [], "C": [], "D": [], "HD": []}
    for s in students:
        avg = Student.from_dict(s.to_dict()).average_mark()
        if avg is None:
            buckets["N/A"].append(f"{s.name} :: {s.id}")
        else:
            g = grade_from_mark(int(round(avg)))
            buckets[g].append(f"{s.name} :: {s.id} --> GRADE: {g} - MARK: {avg:.2f}")

    # Spec for 'g': only print non-empty buckets
    if buckets["N/A"]:
        say(depth, f"N/A --> [{', '.join(buckets['N/A'])}]")
    for k in ["Z", "P", "C", "D", "HD"]:
        if buckets[k]:
            say(depth, f"{k} --> [{', '.join(buckets[k])}]")

def admin_group_pass_fail(depth: int) -> None:
    students = Database.load_students()
    buckets = {"N/A": [], "FAIL": [], "PASS": []}

    for s in students:
        avg = Student.from_dict(s.to_dict()).average_mark()
        if avg is None:
            buckets["N/A"].append(f"{s.name} :: {s.id}")
        else:
            g = "PASS" if avg >= 50.0 else "FAIL"
            grade_letter = grade_from_mark(int(round(avg)))
            buckets[g].append(f"{s.name} :: {s.id} --> GRADE: {grade_letter} - MARK: {avg:.2f}")

    # Spec for 'p': always show all three buckets (even if empty)
    say(depth, f"N/A -->[{', '.join(buckets['N/A'])}]" if buckets["N/A"] else "N/A -->[]")
    say(depth, f"FAIL -->[{', '.join(buckets['FAIL'])}]" if buckets["FAIL"] else "FAIL -->[]")
    say(depth, f"PASS -->[{', '.join(buckets['PASS'])}]" if buckets["PASS"] else "PASS -->[]")

def admin_remove_student(depth: int) -> None:
    sid = ask(depth, "Remove by ID: ")
    students = Database.load_students()
    idx = next((i for i, s in enumerate(students) if s.id == sid), None)
    if idx is None:
        say(depth, f"Student {sid} does not exist", C_RED)
        return
    say(depth, f"Removing Student {sid} Account", C_YELLOW)
    del students[idx]
    Database.save_students(students)

def admin_show_students(depth: int) -> None:
    say(depth, "Student List", C_YELLOW)
    students = Database.load_students()
    if not students:
        say(depth + 2, "<Nothing to Display>")
        return
    for s in students:
        say(depth, f"{s.name} :: {s.id} --> Email: {s.email}")

def admin_menu(depth: int) -> None:
    while True:
        cmd = ask(depth, "Admin System (c/g/p/r/s/x): ", C_SKY).lower()
        if cmd == "c":
            admin_clear(depth)                 # same depth for actions
        elif cmd == "g":
            admin_group_by_grade(depth)        # same depth
        elif cmd == "p":
            admin_group_pass_fail(depth)       # same depth
        elif cmd == "r":
            admin_remove_student(depth)        # same depth
        elif cmd == "s":
            admin_show_students(depth)         # same depth
        elif cmd == "x":
            return
        else:
            say(depth, "Unknown command", C_RED)
