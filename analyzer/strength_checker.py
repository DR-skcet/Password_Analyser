import re
from analyzer.utils import load_common_passwords

def analyze_password(password: str):
    score = 0
    feedback = []

    # Common password check
    if password.lower() in load_common_passwords():
        return 1, "❌ This password is too common."

    # Length
    if len(password) >= 12:
        score += 1
    else:
        feedback.append("🔸 Use at least 12 characters.")

    # Character types
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("🔸 Add uppercase letters.")

    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("🔸 Add lowercase letters.")

    if re.search(r'[0-9]', password):
        score += 1
    else:
        feedback.append("🔸 Include numbers.")

    if re.search(r'[\W_]', password):
        score += 1
    else:
        feedback.append("🔸 Add special characters (!@#...).")

    score = min(score, 5)
    final_feedback = " ".join(feedback) if feedback else "✅ Great job!"
    return score, final_feedback
