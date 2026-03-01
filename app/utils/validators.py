import re

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"
    return True, None

def validate_username(username):
    if len(username) < 3 or len(username) > 50:
        return False, "Username must be 3-50 characters"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username must be alphanumeric with underscores"
    return True, None

def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    return True, None
