import streamlit as st
from analyzer.strength_checker import analyze_password
from analyzer.crack_time_estimator import estimate_crack_time
from analyzer.genai_suggester import suggest_stronger_password
from analyzer.utils import calculate_entropy

st.set_page_config(page_title="🔐 AI Password Strength Analyzer", layout="centered")

# CSS styles for cards & highlights
card_style = """
    <style>
    .card {
        background: #f9f9f9;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgb(0 0 0 / 0.1);
        margin-bottom: 20px;
    }
    .green-text { color: #4caf50; font-weight: bold; }
    .orange-text { color: #ff9800; font-weight: bold; }
    .red-text { color: #f44336; font-weight: bold; }
    </style>
"""
st.markdown(card_style, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🔐 AI-Powered Password Strength Analyzer</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 16px; color: #555;'>Enter your password below to get a detailed strength analysis, estimated crack time, and AI-generated suggestions for improvement.</p>",
    unsafe_allow_html=True
)

password = st.text_input("🔏 Enter Password", type="password", help="Your password is NOT stored or sent anywhere except to the Groq API for suggestions.")

if password:
    score, feedback = analyze_password(password)
    crack_time = estimate_crack_time(password)
    entropy = calculate_entropy(password)
    length = len(password)

    color_map = {
        1: ("red-text", "❌ Very Weak"),
        2: ("orange-text", "⚠️ Weak"),
        3: ("orange-text", "🟡 Medium"),
        4: ("green-text", "✅ Strong"),
        5: ("green-text", "💪 Very Strong"),
    }
    css_class, strength_text = color_map.get(score, ("red-text", "Unknown"))

    st.markdown(f"<div class='card'>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 3])

    with col1:
        st.markdown(f"<h3>Password Strength: <span class='{css_class}'>{strength_text}</span></h3>", unsafe_allow_html=True)
        st.markdown(f"**Score:** {score} / 5")
        st.markdown(f"**Length:** {length} characters")
        st.markdown(f"**Entropy:** {entropy:.2f} bits")

        # Visual meter
        meter = "🟩" * score + "⬜" * (5 - score)
        st.markdown(f"<p style='font-size: 24px'>{meter}</p>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"### ⏳ Estimated Crack Time")
        st.info(f"{crack_time}")

    st.markdown("</div>", unsafe_allow_html=True)

    if score < 4:
        st.markdown(f"<div class='card red-text'><b>Feedback & Tips:</b> {feedback}</div>", unsafe_allow_html=True)

        with st.expander("🤖 AI Suggestions to Improve Password"):
            with st.spinner("Generating suggestions..."):
                suggestion = suggest_stronger_password(password)
            st.markdown("### Suggested Password Alternatives")
            st.code(suggestion)

    # Password checklist
    st.markdown("<h3>🔍 Password Checklist</h3>", unsafe_allow_html=True)
    checklist = {
        "Minimum 12 characters": length >= 12,
        "Contains uppercase letters": any(c.isupper() for c in password),
        "Contains lowercase letters": any(c.islower() for c in password),
        "Includes numbers": any(c.isdigit() for c in password),
        "Includes special characters": any(not c.isalnum() for c in password),
        "Not a common password": score > 1,
        "Entropy > 40 bits": entropy > 40,
    }

    for item, passed in checklist.items():
        icon = "✅" if passed else "❌"
        color = "#4caf50" if passed else "#f44336"
        st.markdown(f"<p style='color: {color}; font-weight: bold'>{icon} {item}</p>", unsafe_allow_html=True)

else:
    st.markdown("<p style='text-align:center; color:#777;'>Enter a password above to start analyzing.</p>", unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: 14px; color:#888;'>Built using Streamlit, Python & Groq API</p>",
    unsafe_allow_html=True
)
