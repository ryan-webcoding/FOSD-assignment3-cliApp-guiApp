import re

EMAIL_RE    = re.compile(r"^[A-Za-z]+[.][A-Za-z]+@university\.com$")
PASSWORD_RE = re.compile(r"^[A-Z][A-Za-z]{4,}\d{3,}$")

def valid_email(email: str) -> bool:
    return EMAIL_RE.match(email) is not None

def valid_password(pw: str) -> bool:
    return PASSWORD_RE.match(pw) is not None

def email_to_name(email: str) -> str:
    local = email.split("@")[0]
    if "." in local:
        first, last = local.split(".", 1)
        return f"{first.capitalize()} {last.capitalize()}"
    return local.capitalize()
