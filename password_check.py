import string

EXCLUDED_SPECIALS = set(';"')  # исключаем ; и двойную кавычку
ALLOWED_SPECIALS = set(string.punctuation) - EXCLUDED_SPECIALS


def check_password(password, min_len: int = 6):
    if len(password) < min_len:
        return False
    has_upper = False
    has_lower = False
    has_special = False

    for ch in password:
        if ch in EXCLUDED_SPECIALS:
            return False
        if "A" <= ch <= "Z":
            has_upper = True
        elif "a" <= ch <= "z":
            has_lower = True
        elif ch in ALLOWED_SPECIALS:
            has_special = True
    return has_upper and has_lower and has_special