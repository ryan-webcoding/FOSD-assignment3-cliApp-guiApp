"""
Entry point for the GUI app.

Run with:
    python -m guiApp.app

This uses the same students.data as the CLI. If you need to override the
location, set env var:  STUDENTS_DATA=/path/to/students.data
"""
from .database_manager import DatabaseManager
from .login_window import LoginWindow

def main():
    db = DatabaseManager()
    app = LoginWindow(db)
    app.mainloop()

if __name__ == "__main__":
    main()
