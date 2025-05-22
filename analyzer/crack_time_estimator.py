import math

def estimate_crack_time(password: str) -> str:
    charset = 0
    if any(c.islower() for c in password): charset += 26
    if any(c.isupper() for c in password): charset += 26
    if any(c.isdigit() for c in password): charset += 10
    if any(not c.isalnum() for c in password): charset += 32

    combinations = charset ** len(password)
    guesses_per_sec = 1e10  # Modern GPU estimate
    seconds = combinations / guesses_per_sec

    years = seconds / (3600 * 24 * 365)

    if years < 1:
        return f"⚠️ Less than a year ({round(years * 12, 2)} months)"
    elif years < 100:
        return f"🟡 ~{int(years)} years"
    else:
        return "🟢 100+ years (very strong)"
