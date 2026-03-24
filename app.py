from flask import Flask, render_template, request
import os

app = Flask(__name__)

questions = [
    "Tell me about yourself",
    "Why should we hire you?",
    "What are your strengths?",
    "What are your weaknesses?",
    "Where do you see yourself in 5 years?",
    "Tell me about your project",
    "What are your goals?"
]

def generate_feedback(answer):
    score = 0
    feedback_points = []

    if "i can" in answer.lower() or "i will" in answer.lower():
       score += 1
       feedback_points.append("Confidence shown.")

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

    if "team" in answer.lower():
        score += 1
        feedback_points.append("Teamwork mentioned.")

    if score >= 8:
        main_feedback = "Excellent answer!"
    elif score >= 5:
        main_feedback = "Good answer!"
    else:
        main_feedback = "Needs improvement."

    ai_feedback = f"""
Your answer shows {main_feedback.lower()}.

Strengths:
- {", ".join([p for p in feedback_points if "mentioned" in p])}

Improvements:
- {", ".join([p for p in feedback_points if "Add" in p or "Mention" in p or "too short" in p])}

Overall, try to give structured answers including skills, projects, and experience with confidence.
"""

    return f"Score: {score}/10\n\n{ai_feedback}"

@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("name")

    return render_template(
        "interview.html",
        question=questions[0],
        q_index=0,
        total=0,
        name=name,
    )
@app.route("/interview", methods=["POST"])
def interview():
    q_index = int(request.form.get("q_index", 0))
    total = int(request.form.get("total", 0))
    answer = request.form.get("answer")

    if answer:
        feedback = generate_feedback(answer)
        score = int(feedback.split("/")[0].split(":")[1])
        total += score

        if q_index + 1 >= len(questions):
            return render_template("final.html", total=total)

        return render_template(
            "result.html",
            feedback=feedback,
            next_q=q_index + 1,
            total=total,
            answer=answer
        )

    return render_template(
        "interview.html",
        question=questions[q_index],
        q_index=q_index,
        total=total
    )
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)