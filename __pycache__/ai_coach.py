# ai_coach.py

def get_question_list(role):
    base_questions = {
        "data scientist": [
            "What is the difference between supervised and unsupervised learning?",
            "How do you handle missing data?",
            "Explain overfitting and how to prevent it."
        ],
        "web developer": [
            "What frameworks have you used for front-end development?",
            "How do you ensure responsive design?",
            "Explain the difference between GET and POST."
        ],
        "default": [
            "Tell me about yourself.",
            "Why do you want this job?",
            "What are your strengths and weaknesses?"
        ]
    }

    return base_questions.get(role.lower(), base_questions["default"])


def evaluate_answer(answer):
    # Placeholder logic (later can add NLP scoring or tone analysis)
    feedback = []

    if len(answer.strip()) < 30:
        feedback.append("Try elaborating more on your response.")
    if any(word in answer.lower() for word in ["team", "project", "experience"]):
        feedback.append("Good! You mentioned teamwork/project experience.")
    else:
        feedback.append("Try including relevant examples from your experience.")

    return feedback
