import tkinter as tk
from tkinter import ttk

class SubjectPopup(tk.Toplevel):
    def __init__(self, parent, subject: dict):
        super().__init__(parent)
        self.title("subject")
        self.resizable(False, False)
        self.configure(padx=24, pady=24)

        self.transient(parent)# so that the pop up always stays on top of enrolment window
        self.grab_set()# so that user must interact or close this pop up before interacting with the enrolment window

        subj_id = subject.get("id")
        title = ttk.Label(self, text=f"subject-{subj_id}", font=("Arial", 22, "bold"))
        title.pack(pady=(0, 16))

        mark_box = ttk.Frame(self, padding=12); mark_box.pack(fill="x", pady=8)
        ttk.Label(mark_box, text=f"mark: {subject.get('mark', '-')}", font=("Arial", 14)).pack()

        grade_box = ttk.Frame(self, padding=12); grade_box.pack(fill="x", pady=8)
        ttk.Label(grade_box, text=f"grade: {subject.get('grade', '-')}", font=("Arial", 14)).pack()

        ttk.Button(self, text="close", command=self.destroy).pack(pady=(16, 0))
        self.bind("<Escape>", lambda e: self.destroy())
        self.wait_visibility(); self.focus_set()
