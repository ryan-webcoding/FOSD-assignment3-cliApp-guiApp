
# Project overview

This project is a simple university management system that allows both students and administrators to interact with a centralized database through two different interfaces:
1. CLI Application: A terminal-based interface for managing students, subjects, and enrollments.
2. GUI Application: A Tkinter-based graphical interface that provides a more user-friendly experience.



## System Requirements
- Python 3.9 or above
- Libraries used:
    - tkinter (for GUI)
    - json (for data persistence)
    - os, sys, and pathlib (for file management)
    - datetime (for timestamps)
    - typing (for type hints)
Works on macOS, Windows, and Linux.
## Installation and setup Instructions
1. Clone or extract the repository:
`git clone https://github.com/ryan-webcoding/FOSD-assignment3-cliApp-guiApp`  
`cd fullAppRepo`  
Or extract the provided ZIP file.  

2. Open the project directory in your IDE or terminal.  

3. Ensure Python is installed:
`python --version`  

4. No external dependencies required (all modules are from Python’s standard library).
## Configuration
students.data file is automatically created under the project directory when the cliApp is first run.  
## How to run, test, use the software
**Run the CLI or GUI Application:**  
Navigate to the parent directory of the project and run:  
`python -m cliApp.app`  
or  
`python -m guiApp.app`