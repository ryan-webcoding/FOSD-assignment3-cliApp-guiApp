import tkinter as tk
from tkinter import ttk, messagebox
from .database_manager import DatabaseManager
from .enrolment_window import EnrolmentWindow

class LoginWindow(tk.Tk):
    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.db = db

        self.title("login")
        self.geometry("820x500")
        self.resizable(False, False)# x and y resizing disabled
        self.configure(padx=28, pady=28)# add outer padding inside window around everything

        # Exit button (top-left)
        ttk.Button(self, text="← exit", command=self._exit_app).grid(row=0, column=0, sticky="w")

        # Title
        ttk.Label(self, text="login", font=("Arial", 26, "bold")).grid(row=0, column=1, columnspan=2, pady=(0, 12))

        # Email
        ttk.Label(self, text="email", font=("Arial", 16, "bold")).grid(row=1, column=0, sticky="e", pady=12, padx=(0, 12))
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(self, textvariable=self.email_var, width=60)
        self.email_entry.grid(row=1, column=1, columnspan=2, sticky="w")
        self.email_entry.focus()

        # Password
        ttk.Label(self, text="password", font=("Arial", 16, "bold")).grid(row=2, column=0, sticky="e", pady=12, padx=(0, 12))
        self.pw_var = tk.StringVar()
        self.pw_entry = ttk.Entry(self, textvariable=self.pw_var, width=60, show="•")
        self.pw_entry.grid(row=2, column=1, columnspan=2, sticky="w")

        # Login button
        ttk.Button(self, text="login!", command=self._handle_login, width=22).grid(row=3, column=1, pady=(24, 0))

        # key bindings
        self.bind("<Return>", lambda e: self._handle_login())

        # balance columns
        self.grid_columnconfigure(1, weight=1)

        self.enrol_window = None  # type: EnrolmentWindow|None

    # --------------- actions ---------------
    def _exit_app(self):
        self.destroy()

    def _handle_login(self):
        email = self.email_var.get().strip()
        pw = self.pw_var.get().strip()

        ok, reason = self.db.authenticate(email, pw)
        if not ok:
            if reason == "empty":
                self._popup_error("email or password is empty")
            elif reason == "no_such_student":
                self._popup_error("Student does not exist")
            elif reason == "bad_password":
                self._popup_error("Incorrect password")
            else:
                self._popup_error("Unknown error")
            return

        # success → open enrolment and hide login window
        self.withdraw()
        self.enrol_window = EnrolmentWindow(self, self.db, email, on_back=self._back_from_enrolment)

    def _back_from_enrolment(self):
        # called by enrolment window when back
        self.deiconify()
        self.email_entry.focus()

    def _popup_error(self, message: str):
        messagebox.showerror("error", message, parent=self)
