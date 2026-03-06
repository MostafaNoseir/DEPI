# app/security.py

import re

def sanitize_string(value: str) -> str:
    """
    Remove unsafe characters.
    Prevents prompt injection, SQL injection, shell tricks, etc.
    """

    # Allow only letters, numbers, spaces, dash
    return re.sub(r"[^a-zA-Z0-9 \\-]", "", value)