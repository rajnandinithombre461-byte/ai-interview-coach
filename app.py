from database import init_db
init_db()

from flask import Flask, render_template, request
from openai import OpenAI
import os
import sqlite3

# ✅ OpenAI setup (safe for Render)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

app = Flask(__name__)

# ✅ Questions
questions = [
    "Tell me about yourself",
    "Why should we hire you?",
    "What are your strengths?",
    "What are your weaknesses?"
]

# ✅ Dummy feedback (safe)
def generate_feedback(answer):
    return "Score: 8/10\nFeedback: Good answer\nImprovement: Improve confidence"


# ✅ Home Page
@app.route("/")
def home():
    return render_template("login.html")


# ✅ Login → Start Interview
@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("name", "Guest")

    return render_template(
        "interview.html",
        question=questions[0],
        q_index=0,
        total=0,
        name=name
    )


# ✅ Interview Route (SAFE VERSION)
@app.route("/interview", methods=["GET", "POST"])
def interview():

    if request.method == "POST":

        # ✅ SAFE DATA FETCH
        answer = request.form.get("answer", "").strip()

        try:
            q_index = int(request.form.get("q_index", 0))
        except:
            q_index = 0

        try:
            total = int(request.form.get("total", 0))
        except:
            total = 0

        name = request.form.get("name", "Guest")

        # ✅ HANDLE EMPTY ANSWER
        if answer == "":
            answer = "No answer provided"

        # ✅ GENERATE FEEDBACK
        feedback = generate_feedback(answer)

        # ✅ EXTRACT SCORE SAFELY
        score = 5
        if "Score:" in feedback:
            try:
                score = int(feedback.split("/")[0].split(":")[1])
            except:
                score = 5

        total += score

        # ✅ FINAL QUESTION → SAVE
        if q_index + 1 >= len(questions):

            conn = sqlite3.connect("interview.db")
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO results (name, score) VALUES (?, ?)",
                (name, total)
            )

            conn.commit()
            conn.close()

            return render_template("final.html", total=total, name=name)

        # ✅ NEXT QUESTION (IMPORTANT FIX)
        return render_template(
            "interview.html",
            question=questions[q_index + 1],
            q_index=q_index + 1,
            total=total,
            name=name
        )

    # ✅ GET REQUEST (FIRST LOAD SAFE)
    if request.method == "GET":
     return render_template(
        "interview.html",
        question=questions[0],
        q_index=0,
        total=0,
        name="Guest"
    )

# ✅ VIEW RAW DATA
@app.route("/data")
def show_data():
    conn = sqlite3.connect("interview.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM results")
    rows = cursor.fetchall()

    conn.close()

    return str(rows)


# ✅ ADMIN PANEL
@app.route("/admin")
def admin():
    conn = sqlite3.connect("interview.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM results")
    data = cursor.fetchall()

    conn.close()

    return render_template("admin.html", data=data)


# ✅ RUN SERVER (LOCAL ONLY)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)