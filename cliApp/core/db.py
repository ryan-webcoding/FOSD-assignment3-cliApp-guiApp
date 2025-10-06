import json, os
from typing import List
from .models import Student

DATA_FILE = "students.data"  # unchanged

class Database:
    @staticmethod
    def ensure_file() -> None:
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)

    @staticmethod
    def load_students() -> List[Student]:
        Database.ensure_file()
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                raw = json.load(f)
            except json.JSONDecodeError:
                raw = []
        return [Student.from_dict(r) for r in raw]

    @staticmethod
    def save_students(students: List[Student]) -> None:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in students], f, indent=2)

    @staticmethod
    def clear() -> None:
        Database.save_students([])
