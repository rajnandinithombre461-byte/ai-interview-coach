from flask import Flask, render_template, request
import os

app = Flask(__name__)

questions = [
    "Tell me about yourself",
    "Why should we hire you?",
    "What are your strengths?",
    "What are your weaknesses?"
]

def generate_feedback(answer):
    score = 5
    feedback = "Good attempt!"

    if len(answer) > 50:
        score += 2
    if "skills" in answer.lower():
        score += 1
    if "project" in answer.lower():
        score += 1
    if "experience" in answer.lower():
        score += 1

    return f"Score: {score}/10\n{feedback}"

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    return render_template("interview.html", question=questions[0], q_index=0, total=0)

@app.route("/interview", methods=["POST"])
def interview():
    q_index = int(request.form["q_index"])
    total = int(request.form["total"])
    answer = request.form["answer"]

    feedback = generate_feedback(answer)
    score = int(feedback.split("/")[0].split(":")[1])
    total += score

    if q_index + 1 >= len(questions):
        return render_template("final.html", total=total)

    return render_template("result.html",
                           feedback=feedback,
                           next_q=q_index + 1,
                           total=total)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)