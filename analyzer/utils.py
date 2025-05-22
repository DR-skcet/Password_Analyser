import math

def load_common_passwords():
    with open("data/common_passwords.txt", "r") as file:
        return set(line.strip().lower() for line in file.readlines())

def calculate_entropy(password: str) -> float:
    charset = 0
    if any(c.islower() for c in password): charset += 26
    if any(c.isupper() for c in password): charset += 26
    if any(c.isdigit() for c in password): charset += 10
    if any(not c.isalnum() for c in password): charset += 32
    if charset == 0:
        return 0.0
    return len(password) * math.log2(charset)