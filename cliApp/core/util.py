import random
from typing import List

def gen_student_id(existing_ids: List[str]) -> str:
    while True:
        sid = f"{random.randint(1, 999999):06d}"
        if sid not in existing_ids:
            return sid

def gen_subject_id(existing_ids_for_student: List[str]) -> str:
    while True:
        sid = f"{random.randint(1, 999):03d}"
        if sid not in existing_ids_for_student:
            return sid
