# ai_coach.py

def get_question_list(role):
    if role.lower() == "data analyst":
        return [
            "What steps do you follow when cleaning data?",
            "How do you handle missing values in a dataset?",
            "Explain a project where you used SQL for data extraction.",
        ]
    elif role.lower() == "software engineer":
        return [
            "Tell me about a challenging bug you fixed.",
            "How do you ensure code quality in your projects?",
            "Describe your experience with version control tools.",
        ]
    else:
        return [
            "Tell me about yourself.",
            "What are your strengths and weaknesses?",
            "Why should we hire you?",
        ]

def evaluate_answer(answer):
    if len(answer.strip()) < 10:
        return "Try elaborating more on your answer."
    elif "team" in answer.lower():
        return "Great! Highlighting teamwork is a plus."
    else:
        return "Good answer. Consider adding more specific examples."
