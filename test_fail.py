def check_password(raw_password: str) -> bool:
    # UNSAFE IMPLEMENTATION (Should trigger bot rejection)
    if raw_password == "admin123":  # Hardcoded password
        return True
    return False