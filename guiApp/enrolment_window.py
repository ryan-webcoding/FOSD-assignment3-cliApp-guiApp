import tkinter as tk
from tkinter import ttk, messagebox
from .database_manager import DatabaseManager
from .subject_popup import SubjectPopup

class EnrolmentWindow(tk.Toplevel):
    def __init__(self, parent, db: DatabaseManager, email: str, on_back):
        super().__init__(parent)
        self.db = db
        self.email = email
        self.on_back = on_back

        self.title("enrolment")
        self.geometry("720x520")
        self.configure(padx=20, pady=20)

        ttk.Button(self, text="←", width=3, command=self._back).grid(row=0, column=0, sticky="w")
        ttk.Label(self, text="enrolment", font=("Arial", 22, "bold")).grid(row=0, column=1, columnspan=2, pady=(0, 10))

        self.list_frame = ttk.Frame(self, padding=4)
        self.list_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=(8, 8))
        self.grid_rowconfigure(1, weight=1); self.grid_columnconfigure(1, weight=1)

        ttk.Button(self, text="enrol", command=self._enrol_one, width=18).grid(row=2, column=1, pady=(8, 0))

        self._refresh_list()
        self.protocol("WM_DELETE_WINDOW", self._back) # upon clicking the "X" button, call self.back()

    def _back(self):
        self.destroy()
        if callable(self.on_back):
            self.on_back()

    def _enrol_one(self):
        try:
            _ = self.db.enrol_new_subject(self.email)
            self._refresh_list()
        except ValueError as e:
            if str(e) == "limit_reached":
                self._popup_error("each student can only enrol in 4 subject maximum")
            else:
                self._popup_error("unknown error while enrolling")

    def _popup_error(self, message: str):
        messagebox.showerror("error", message, parent=self)

    def _refresh_list(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        student = self.db.get_student(self.email)
        subjects = student.get("subjects", [])

        for row, s in enumerate(subjects):
            row_frame = ttk.Frame(self.list_frame, padding=6)
            row_frame.grid(row=row, column=0, sticky="ew", pady=6)
            self.list_frame.grid_columnconfigure(0, weight=1)

            subj_id_str = str(s.get("id")) if s.get("id") is not None else "?"
            ttk.Button(row_frame, text=f"Subject-{subj_id_str}",
                       command=lambda subj=s: self._open_subject(subj)
                       ).pack(side="left", padx=(0, 10))

            ttk.Button(row_frame, text="🗑", width=3,
                       command=lambda sid=subj_id_str: self._delete_subject(sid)
                       ).pack(side="right")

    def _open_subject(self, subject: dict):
        SubjectPopup(self, subject)

    def _delete_subject(self, subject_id: str):
        self.db.delete_subject(self.email, subject_id)
        self._refresh_list()
