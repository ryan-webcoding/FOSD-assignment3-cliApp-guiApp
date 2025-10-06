from typing import Dict, List, Optional

def grade_from_mark(mark: int) -> str:
    if mark < 50:    return "Z"
    if mark < 65:    return "P"
    if mark < 75:    return "C"
    if mark < 85:    return "D"
    return "HD"

class Subject:
    def __init__(self, sid: str, mark: int, grade: str):
        self.id = sid
        self.mark = mark
        self.grade = grade

    def to_dict(self) -> Dict:
        return {"id": self.id, "mark": self.mark, "grade": self.grade}

    @staticmethod
    def from_dict(d: Dict) -> "Subject":
        return Subject(d["id"], int(d["mark"]), d["grade"])

class Student:
    def __init__(self, sid: str, name: str, email: str, password: str, subjects: Optional[List[Subject]] = None):
        self.id = sid
        self.name = name
        self.email = email
        self.password = password
        self.subjects: List[Subject] = subjects or []

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "subjects": [s.to_dict() for s in self.subjects],
        }

    @staticmethod
    def from_dict(d: Dict) -> "Student":
        subs = [Subject.from_dict(s) for s in d.get("subjects", [])]
        return Student(d["id"], d["name"], d["email"], d["password"], subs)

    # Business rules
    def can_enrol_more(self) -> bool:
        return len(self.subjects) < 4

    def has_subject_id(self, sid: str) -> bool:
        return any(s.id == sid for s in self.subjects)

    def add_subject(self, s: Subject) -> None:
        if self.can_enrol_more():
            self.subjects.append(s)

    def remove_subject(self, sid: str) -> bool:
        for i, s in enumerate(self.subjects):
            if s.id == sid:
                del self.subjects[i]
                return True
        return False

    def average_mark(self) -> Optional[float]:
        if not self.subjects:
            return None
        return sum(s.mark for s in self.subjects) / len(self.subjects)

    def grade_from_average(self) -> Optional[str]:
        avg = self.average_mark()
        if avg is None:
            return None
        return grade_from_mark(int(round(avg)))
