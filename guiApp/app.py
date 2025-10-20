"""
Entry point for the GUI app.

Run with:
    python -m guiApp.app
"""
from .database_manager import DatabaseManager
from .login_window import LoginWindow

def main():
    db = DatabaseManager()
    app = LoginWindow(db)
    app.mainloop()

if __name__ == "__main__":
    main()
