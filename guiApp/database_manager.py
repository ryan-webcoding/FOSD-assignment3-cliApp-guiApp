# guiApp/database_manager.py
from __future__ import annotations
import json, os, random
from typing import Dict, List, Optional, Tuple

# ----------------------------- public helpers -----------------------------

def grade_from_mark(mark: int) -> str:
    if mark >= 85: return "HD"
    if mark >= 75: return "D"
    if mark >= 65: return "C"
    if mark >= 50: return "P"
    return "Z"

# ------------------------------ data manager ------------------------------

class DatabaseManager:
    """
    Minimal persistence for a single JSON layout:

    students.data (list-root):
    [
      { "id": "561005", "name": "...", "email": "...", "password": "...",
        "subjects": [ { "id": "017", "mark": 36, "grade": "Z" }, ... ] },
      ...
    ]

    Path: project_root/students.data  (project_root contains the guiApp/ folder)
    """

    def __init__(self, data_path: Optional[str] = None):
        # Default: <project_root>/students.data, where project_root is the parent of guiApp/
        pkg_dir = os.path.dirname(os.path.abspath(__file__))   # find the folder where database_manager.py is at
        project_root = os.path.dirname(pkg_dir)                # go one level up to the main project folder
        self.path = data_path or os.path.join(project_root, "students.data") # if user provided a path, use that, other wise use project_root to store "students.data"
        self._ensure_file()

    # ----------------------------- public API -----------------------------
    # user would login 
    def authenticate(self, email: str, password: str) -> Tuple[bool, str]:
        """
        Returns (ok, code). Codes: "empty" | "no_such_student" | "bad_password" | "" (success)
        """
        email = (email or "").strip()
        password = (password or "").strip()
        if not email or not password:
            return False, "empty"

        student = self._find_student_by_email(email)
        if not student:
            return False, "no_such_student"
        if student.get("password") != password:
            return False, "bad_password"
        return True, ""

    def get_student(self, email: str) -> Dict:
        """Return the student dict for an email or raise KeyError."""
        student = self._find_student_by_email(email)
        if not student:
            raise KeyError("Student not found")
        # Ensure subjects list exists
        student.setdefault("subjects", [])
        return student

    def save_student(self, student: Dict) -> None:
        """
        Upsert by email.
        If a student with the same email exists, replace it; otherwise append.
        """
        students = self._read()
        for i, s in enumerate(students):
            if s.get("email") == student.get("email"):
                students[i] = student
                self._write(students)
                return
        students.append(student)
        self._write(students)

    def enrol_new_subject(self, email: str) -> Dict:
        """
        Add a new subject with a unique 3-digit string id ("000".."999"),
        random mark (25..100), and computed grade.
        Limit: 4 subjects per student (raises ValueError("limit_reached")).
        """
        student = self.get_student(email)
        subjects: List[Dict] = student.setdefault("subjects", []) #if there are subject list already, return it; otherwise create an empty list
        if len(subjects) >= 4:
            raise ValueError("limit_reached")

        new_id = self._random_subject_id(subjects)  # "000".."999"
        mark = random.randint(25, 100)
        grade = grade_from_mark(mark)
        new_subject = {"id": new_id, "mark": mark, "grade": grade}
        subjects.append(new_subject)
        self.save_student(student)
        return new_subject

    def delete_subject(self, email: str, subject_id) -> None:
        """Delete a subject by its id (string or int accepted)."""
        student = self.get_student(email)
        sid = str(subject_id).zfill(3) if str(subject_id).isdigit() else str(subject_id)
        before = len(student.get("subjects", []))
        student["subjects"] = [s for s in student.get("subjects", []) if str(s.get("id")) != sid]
        if len(student["subjects"]) != before:
            self.save_student(student)

    # ----------------------------- internals ------------------------------

    def _ensure_file(self) -> None:
        """Create an empty list file if missing; otherwise leave as-is."""
        if not os.path.exists(self.path):
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            self._write([])

    def _read(self) -> List[Dict]:
        """Always returns a list of students."""
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Be strict: expect a list; if not, reset to empty list.
        return data if isinstance(data, list) else []

    def _write(self, students: List[Dict]) -> None:
        """Overwrite the file with the list of students (pretty-printed)."""
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(students, f, indent=2)

    def _find_student_by_email(self, email: str) -> Optional[Dict]:
        """Exact match on email (case-sensitive)."""
        for s in self._read():
            if s.get("email") == email:
                # Return a *fresh* object; callers may mutate and then call save_student
                return s
        return None

    # ---- subject ID generation (3-digit strings "000".."999") ----

    @staticmethod
    def _format_id(n: int) -> str:
        return f"{n:03d}"

    def _used_ids(self, subjects: List[Dict]) -> set:
        return {str(s.get("id")).zfill(3) for s in subjects if s.get("id") is not None and str(s.get("id")).isdigit()}

    def _random_subject_id(self, subjects: List[Dict]) -> str:
        """Pick an unused 3-digit id. Try random picks; fallback to linear."""
        used = self._used_ids(subjects)
        # If saturated (unlikely), grow beyond 999 linearly.
        if len(used) >= 1000:
            n = 1000
            while self._format_id(n) in used:
                n += 1
            return self._format_id(n)

        # Try random first for nicer distribution
        for _ in range(1000):
            n = random.randint(0, 999)
            cand = self._format_id(n)
            if cand not in used:
                return cand

        # Fallback: linear probe
        n = 0
        while self._format_id(n) in used:
            n += 1
        return self._format_id(n)
