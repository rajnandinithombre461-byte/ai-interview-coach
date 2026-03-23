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
    score = 0
    feedback_points = []

    if len(answer) > 50:
        score += 2
        feedback_points.append("Good detailed answer.")
    else:
        feedback_points.append("Answer is too short.")

    if "skill" in answer.lower():
        score += 2
        feedback_points.append("Skills mentioned.")
    else:
        feedback_points.append("Add your skills.")

    if "project" in answer.lower():
        score += 2
        feedback_points.append("Projects included.")
    else:
        feedback_points.append("Mention your projects.")

    if "experience" in answer.lower():
        score += 2
        feedback_points.append("Experience mentioned.")
    else:
        feedback_points.append("Add your experience.")

    if score >= 8:
        main_feedback = "Excellent answer!"
    elif score >= 5:
        main_feedback = "Good answer!"
    else:
        main_feedback = "Needs improvement."

    return f"Score: {score}/10\n{main_feedback}\n\n" + "\n".join(feedback_points)


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    return render_template("interview.html",
                           question=questions[0],
                           q_index=0,
                           total=0)


@app.route("/interview", methods=["POST"])
def interview():
    q_index = int(request.form.get("q_index", 0))
    total = int(request.form.get("total", 0))
    answer = request.form.get("answer")

    # ✅ If answer exists (Submit clicked)
    if answer:
        feedback = generate_feedback(answer)
        score = int(feedback.split("/")[0].split(":")[1])
        total += score

        if q_index + 1 >= len(questions):
            return render_template("final.html", total=total)

        return render_template("result.html",
                               feedback=feedback,
                               next_q=q_index + 1,
                               total=total,
                               answer=answer)

    # ✅ If Next button clicked (no answer)
    return render_template("interview.html",
                           question=questions[q_index],
                           q_index=q_index,
                           total=total)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)