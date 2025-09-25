import streamlit as st
import json
import os
import re

# 🌄 Background + Animations + Styling
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://i.postimg.cc/3wMgf5MN/OIP-1.webp");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.4);
        z-index: -1;
    }

    @keyframes glow {
        0% { text-shadow: 0 0 5px white; }
        50% { text-shadow: 0 0 20px white; }
        100% { text-shadow: 0 0 5px white; }
    }
    .glow-text {
        animation: glow 2s infinite;
        font-size: 20px;
        color: white;
        font-family: Georgia;
        text-align: center;
        margin-top: 20px;
    }

    @keyframes float {
        0% { transform: translateY(0); opacity: 1; }
        100% { transform: translateY(100vh); opacity: 0; }
    }
    .leaf {
        position: fixed;
        top: -50px;
        left: calc(10% + 80px * var(--i));
        font-size: 24px;
        animation: float 10s linear infinite;
        animation-delay: calc(1s * var(--i));
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    .earth {
        text-align: center;
        font-size: 30px;
        animation: pulse 2s infinite;
        margin-top: 10px;
    }

    /* 🌟 Radio options styled like white cards */
    div[data-baseweb="radio"] label {
        font-size: 22px !important;
        font-weight: bold !important;
        font-family: Georgia, serif !important;
        color: black !important;
        background: white !important;
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 10px;
        display: block;
        cursor: pointer;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    div[data-baseweb="radio"] label:hover {
        background: #f0f0f0 !important;
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }

    /* 🔵 Blue button style */
    .stButton button {
        background-color: #007bff !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: bold !important;
        padding: 10px 25px !important;
        border-radius: 10px !important;
        border: none !important;
        cursor: pointer !important;
        transition: transform 0.2s, background-color 0.2s;
    }
    .stButton button:hover {
        background-color: #0056b3 !important;
        transform: scale(1.05);
    }
    </style>

    <div class="leaf" style="--i:0;">🍃</div>
    <div class="leaf" style="--i:1;">🍂</div>
    <div class="leaf" style="--i:2;">🍃</div>
    <div class="earth">🌍</div>
    <p class="glow-text">Let’s protect our planet while we learn! 🌿</p>
""", unsafe_allow_html=True)

# 🌱 Bold White Title
st.markdown("""
<h1 style='text-align: center; color: white; font-family: Arial Black, sans-serif; font-size: 42px; font-weight: bold;'>
EVS QUIZZES
</h1>
""", unsafe_allow_html=True)

# 📚 Load questions
def load_questions():
    with open("evs_questions.json", "r") as f:
        return json.load(f)

questions = load_questions()

# 🧠 Session state
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.name = ""
    st.session_state.submitted = False

# 🙋 Ask for name with validation
if st.session_state.name == "":
    st.markdown("<p style='font-size:18px; font-family: Verdana; color:white;'>Enter your name to begin:</p>", unsafe_allow_html=True)
    name_input = st.text_input("")
    if len(name_input.strip()) >= 2 and re.match("^[A-Za-z ]+$", name_input):
        st.session_state.name = name_input.strip()
    else:
        st.markdown("<p style='color:red;'>Please enter a valid name (at least 2 letters, no symbols).</p>", unsafe_allow_html=True)
    st.stop()

# ❓ Show question
if st.session_state.q_index < len(questions):
    q = questions[st.session_state.q_index]
    correct_answer = q["options"][q["answer"][0]]

    st.markdown(f"<h3 style='color:white; font-family: Georgia; font-size:24px;'>{q['question']}</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:20px; font-family: Verdana; color:white;'>Choose your answer:</p>", unsafe_allow_html=True)

    selected = st.radio("", q["options"], index=None)

    if not st.session_state.submitted and st.button("Submit"):
        if selected == correct_answer:
            st.session_state.score += 1
            st.markdown("<p style='color:lightgreen; font-size:20px; font-weight:bold;'>✅ Correct!</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='color:red; font-size:20px; font-weight:bold;'>❌ Wrong! Correct answer: {correct_answer}</p>", unsafe_allow_html=True)

        st.markdown(f"<p style='color:white; font-size:18px;'>📘 Explanation: {q['explanation']}</p>", unsafe_allow_html=True)
        st.session_state.submitted = True

    elif st.session_state.submitted and st.button("Next Question"):
        st.session_state.q_index += 1
        st.session_state.submitted = False
        st.rerun()

# 🏁 Final Score + Leaderboard
else:
    st.success(f"🎉 Quiz completed! Your score: {st.session_state.score}/{len(questions)}")
    st.balloons()

    def save_score(name, score):
        scores = []
        if os.path.exists("scores.json"):
            with open("scores.json", "r") as f:
                scores = json.load(f)
        scores.append({"name": name, "score": score})
        with open("scores.json", "w") as f:
            json.dump(scores, f)

    save_score(st.session_state.name, st.session_state.score)

    st.markdown("<h2 style='color:white; font-family: Lucida Console;'>🏆 Leaderboard</h2>", unsafe_allow_html=True)
    with open("scores.json", "r") as f:
        scores = json.load(f)
        sorted_scores = sorted(scores, key=lambda x: x["score"], reverse=True)
        for entry in sorted_scores[:5]:
            st.markdown(f"<div style='font-size:20px; color:white; font-family: Lucida Console;'>🏅 <b>{entry['name']}</b> — {entry['score']} pts</div>", unsafe_allow_html=True)

    st.markdown("""
    <form action="">
        <button class="restart-btn">Restart Quiz</button>
    </form>
    """, unsafe_allow_html=True)

    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.name = ""
    st.session_state.submitted = False