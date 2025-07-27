import os
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader

# AI Interview Coach functions
from ai_coach import get_question_list, evaluate_answer

# Initialize Flask App
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ---------- ROUTES ----------

# Home
@app.route('/')
def home():
    return render_template('home.html')

# Resume Analyzer Page
@app.route('/resume-analyzer')
def resume_analyzer():
    return render_template('resume_analyzer.html')

# Interview Coach Page (Landing)
@app.route('/interview-coach')
def interview_coach():
    return render_template('interview_coach.html')

# Mock Interview Page
@app.route('/mock-interview')
def mock_interview():
    return render_template('mock_interview.html')

# ---------- UTILITIES ----------

# PDF Text Extractor
def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ''
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

# Generate Questions from Resume
def generate_interview_questions(text):
    questions = []
    if 'Python' in text:
        questions.append("Can you explain your experience with Python?")
    if 'Machine Learning' in text:
        questions.append("Which ML models have you worked with?")
    if 'SQL' in text:
        questions.append("How have you used SQL in your projects?")
    if 'Leadership' in text:
        questions.append("Describe a situation where you showed leadership.")
    if 'Communication' in text:
        questions.append("How do you handle team communication in tough situations?")
    if not questions:
        questions.append("Can you tell us more about your recent projects?")
    return questions

# ---------- RESUME ANALYZER FUNCTIONALITY ----------

@app.route('/analyze-resume', methods=['POST'])
def analyze_resume():
    if 'resume' not in request.files:
        return redirect(request.url)

    resume = request.files['resume']
    if resume.filename == '':
        return redirect(request.url)

    if resume:
        filename = secure_filename(resume.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        resume.save(filepath)

        # Extract and highlight keywords
        extracted_text = extract_text_from_pdf(filepath)
        keywords = ['Python', 'Java', 'Machine Learning', 'Data Analysis',
                    'Leadership', 'Communication', 'SQL', 'Flask', 'Teamwork']

        highlighted_text = extracted_text
        for kw in keywords:
            highlighted_text = highlighted_text.replace(kw, f"<mark>{kw}</mark>")

        questions = generate_interview_questions(extracted_text)

        return render_template(
            'resume_analyzer.html',
            extracted_text=highlighted_text,
            questions=questions
        )

# ---------- AI INTERVIEW COACH FUNCTIONALITY ----------

@app.route('/interview', methods=['GET', 'POST'])
def interview():
    if request.method == 'POST':
        if 'start' in request.form:
            role = request.form.get('role', 'general')  # Default role
            session['questions'] = get_question_list(role)
            session['current'] = 0
            session['qa'] = []
            return redirect(url_for('interview'))

        if 'answer' in request.form:
            answer = request.form.get('answer')
            index = session['current']
            question = session['questions'][index]
            feedback = evaluate_answer(answer)
            session['qa'].append({
                'question': question,
                'answer': answer,
                'feedback': feedback
            })
            session['current'] += 1

    if 'questions' not in session or session['current'] >= len(session['questions']):
        return render_template('interview_summary.html', qa=session.get('qa', []))

    question = session['questions'][session['current']]
    return render_template('interview.html', question=question)
if __name__ == '__main__':
    app.run(debug=True)
