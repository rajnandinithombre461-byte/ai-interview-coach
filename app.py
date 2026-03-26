from database import init_db
init_db()

from flask import Flask, render_template, request
from openai import OpenAI
import os
import sqlite3

# ✅ OpenAI setup
client = OpenAI(api_key="YOUR_API_KEY_HERE")

app = Flask(__name__)

# ✅ Questions
questions = [
    "Tell me about yourself",
    "Why should we hire you?",
    "What are your strengths?",
    "What are your weaknesses?"
]

def generate_feedback(answer):
    return "Score: 8/10\nFeedback: Good answer\nImprovement: Improve confidence"


# ✅ Home Page
@app.route("/")
def home():
    return render_template("login.html")


# ✅ Login → Start Interview
@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("name")  # ✅ get user name
    return render_template(
        "interview.html",
        question=questions[0],
        q_index=0,
        total=0,
        name=name
    )


# ✅ Interview Logic
@app.route("/interview", methods=["GET", "POST"])
def interview():

    if request.method == "POST":
        answer = request.form["answer"]
        q_index = int(request.form["q_index"])
        total = int(request.form["total"])
        name = request.form.get("name")  # ✅ IMPORTANT

        feedback = generate_feedback(answer)

        # ✅ Extract score
        score = 5
        if "Score:" in feedback:
            try:
                score = int(feedback.split("/")[0].split(":")[1])
            except:
                score = 5

        total += score

        # ✅ FINAL QUESTION → SAVE TO DATABASE
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

        # ✅ NEXT QUESTION
        else:
            return render_template(
                "result.html",
                feedback=feedback,
                next_q=q_index + 1,
                total=total,
                answer=answer,
                name=name
            )

    # ✅ FIRST LOAD (GET)
    name = request.args.get("name", "Candidate")

    return render_template(
        "interview.html",
        question=questions[0],
        q_index=0,
        total=0,
        name=name
    )

@app.route("/data")
def show_data():
    import sqlite3
    conn = sqlite3.connect("interview.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM results")
    rows = cursor.fetchall()

    conn.close()

    return str(rows)

@app.route("/admin")
def admin():
    import sqlite3
    conn = sqlite3.connect("interview.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM results")
    data = cursor.fetchall()

    conn.close()

    return render_template("admin.html", data=data)


# ✅ RUN SERVER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)