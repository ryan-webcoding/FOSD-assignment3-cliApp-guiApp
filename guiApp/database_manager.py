from __future__ import annotations
import json, os, random, re
from typing import Dict, List, Optional, Tuple, Union

def grade_from_mark(mark: int) -> str:
    if mark >= 85: return "HD"
    if mark >= 75: return "D"
    if mark >= 65: return "C"
    if mark >= 50: return "P"
    return "Z"

JsonType = Union[Dict, List]
_SUBJ_STR_RE = re.compile(r"^Subject-(\d{1,3})$")

class DatabaseManager:
    """
    Supports both JSON shapes:

    A) LIST-ROOT (CLI style)
       [ {"email":"...","password":"...","subjects":[...]}, ... ]

    B) DICT-ROOT
       {"students":[ {...}, {...} ]}
    """
    def __init__(self, data_path: Optional[str] = None):
        env_path = os.getenv("STUDENTS_DATA")
        if env_path:
            self.path = env_path
        elif data_path:
            self.path = data_path
        else:
            pkg_dir = os.path.dirname(os.path.abspath(__file__))
            self.path = os.path.normpath(os.path.join(pkg_dir, "..", "students.data"))

        self._root_style = "list"  # "list" or "dict"
        self._ensure_file()

    # ----------------- public API -----------------
    def authenticate(self, email: str, password: str) -> Tuple[bool, str]:
        email = (email or "").strip()
        password = (password or "").strip()
        if not email or not password:
            return False, "empty"

        data = self._read()
        students = self._students(data)
        student = self._find_student(students, email)
        if not student:
            return False, "no_such_student"
        if student.get("password") != password:
            return False, "bad_password"
        return True, ""

    def get_student(self, email: str) -> Dict:
        data = self._read()
        students = self._students(data)
        student = self._find_student(students, email)
        if not student:
            raise KeyError("Student not found")
        if self._normalize_student_subjects(student):
            # persist normalization (e.g., 123 -> "123", "Subject-456" -> "456")
            self._write(data, students)
        student.setdefault("subjects", [])
        return student

    def save_student(self, student: Dict) -> None:
        data = self._read()
        students = self._students(data)
        for i, s in enumerate(students):
            if s.get("email") == student.get("email"):
                students[i] = student
                break
        else:
            students.append(student)
        self._write(data, students)

    def enrol_new_subject(self, email: str) -> Dict:
        """Add one subject (id = random string '0'..'999' unique for this student)."""
        student = self.get_student(email)
        subjects: List[Dict] = student.setdefault("subjects", [])
        if len(subjects) >= 4:
            raise ValueError("limit_reached")

        new_id_str = self._random_subject_id(subjects)  # string
        mark = random.randint(25, 100)
        grade = grade_from_mark(mark)
        new_subject = {"id": new_id_str, "mark": mark, "grade": grade}
        subjects.append(new_subject)
        self.save_student(student)
        return new_subject

    def delete_subject(self, email: str, subject_id) -> None:
        student = self.get_student(email)
        sid = str(subject_id)  # compare as string
        before = len(student.get("subjects", []))
        student["subjects"] = [s for s in student.get("subjects", []) if str(s.get("id")) != sid]
        if len(student["subjects"]) != before:
            self.save_student(student)

    # ----------------- helpers -----------------
    def _ensure_file(self):
        if not os.path.exists(self.path):
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            self._root_style = "list"
            self._write([], [])
            return

        try:
            data = self._read()
            if isinstance(data, list):
                self._root_style = "list"
            elif isinstance(data, dict):
                self._root_style = "dict"
            else:
                self._root_style = "list"
                self._write([], [])
        except Exception:
            self._root_style = "list"
            self._write([], [])

    def _read(self) -> JsonType:
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _students(self, data: JsonType) -> List[Dict]:
        if isinstance(data, list):
            self._root_style = "list"
            return data
        if isinstance(data, dict):
            self._root_style = "dict"
            return data.get("students", [])
        self._root_style = "list"
        return []

    def _write(self, data: JsonType, students_list: List[Dict]) -> None:
        if self._root_style == "dict":
            out: JsonType = {"students": students_list}
        else:
            out = students_list
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2)

    @staticmethod
    def _find_student(students: List[Dict], email: str) -> Optional[Dict]:
        for s in students:
            if isinstance(s, dict) and s.get("email") == email:
                return s
        return None

    # --- Subject id handling (store as STRING) ---
    @staticmethod
    def _extract_numeric_id(raw) -> Optional[str]:
        """
        Accept int -> return numeric string;
        Accept 'Subject-###' -> return '###';
        Accept numeric string -> return it;
        Else None.
        """
        if isinstance(raw, int):
            return str(raw)
        if isinstance(raw, str):
            if raw.isdigit():
                return raw
            m = _SUBJ_STR_RE.match(raw)
            if m:
                return m.group(1)
        return None

    def _normalize_student_subjects(self, student: Dict) -> bool:
        """Convert any int or 'Subject-###' ids to pure numeric strings. Returns True if changed."""
        changed = False
        subs = student.setdefault("subjects", [])
        for s in subs:
            normalized = self._extract_numeric_id(s.get("id"))
            if normalized is not None and s.get("id") != normalized:
                s["id"] = normalized
                changed = True
        return changed

    @staticmethod
    def _used_ids(subjects: List[Dict]) -> set:
        # set of numeric-string ids
        used = set()
        for s in subjects:
            nid = s.get("id")
            if nid is None: 
                continue
            used.add(str(nid))
        return used

    def _random_subject_id(self, subjects: List[Dict]) -> str:
        """Pick a random unused numeric-string in [0, 999]."""
        used = self._used_ids(subjects)
        if len(used) >= 1000:
            # Extremely unlikely; expand space
            n = 1000
            while str(n) in used:
                n += 1
            return str(n)
        for _ in range(1000):
            candidate = str(random.randint(0, 999))
            if candidate not in used:
                return candidate
        # Fallback linear probe
        i = 0
        while str(i) in used:
            i += 1
        return str(i)
