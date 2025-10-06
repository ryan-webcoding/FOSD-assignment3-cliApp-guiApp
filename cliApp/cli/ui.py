from typing import Optional

RESET   = "\033[0m"
C_SKY   = "\033[96m"  # bright cyan
C_YELLOW= "\033[93m"
C_RED   = "\033[91m"
C_GREEN = "\033[92m"

# Jump size (in "depth levels") when entering a submenu.
# Each depth level is 2 spaces (see indent_str), so 4 levels = 8 spaces.
SUBMENU_STEP = 4

def colour(text: str, c: str) -> str:
    return f"{c}{text}{RESET}"

def indent_str(depth: int) -> str:
    return "  " * depth  # two spaces per level

def say(depth: int, text: str, c: Optional[str] = None) -> None:
    if c:
        print(indent_str(depth) + colour(text, c))
    else:
        print(indent_str(depth) + text)

def ask(depth: int, prompt_text: str, c: Optional[str] = None) -> str:
    prompt = indent_str(depth) + (colour(prompt_text, c) if c else prompt_text)
    return input(prompt).strip()
