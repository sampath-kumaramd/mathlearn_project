# app.py

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
from dotenv import load_dotenv
import json
import config

# Load environment variables
load_dotenv()

# Import custom modules
from src.nlp.enhanced_tokenizer import EnhancedSinhalaTokenizer
from src.tts.enhanced_speech_engine import EnhancedSpeechEngine
from src.learning.student_profile import StudentProfile
from src.learning.lesson_generator import AdaptiveLessonGenerator
from src.cultural.problem_generator import CulturalProblemGenerator
from src.feedback.feedback_engine import FeedbackEngine

# Create Flask app once with all configurations
template_dir = os.path.abspath('templates')
app = Flask(__name__, template_folder=template_dir)
app.secret_key = config.SECRET_KEY  # Set the secret key

# Initialize components
tokenizer = EnhancedSinhalaTokenizer()
speech_engine = EnhancedSpeechEngine(language='si')
problem_generator = CulturalProblemGenerator()
lesson_generator = AdaptiveLessonGenerator()
feedback_engine = FeedbackEngine(speech_engine, language='si')

# Global cache for student profiles
student_profiles = {}

def get_student_profile(student_id, impairment_type=1):
    """Get or create student profile"""
    if student_id not in student_profiles:
        student_profiles[student_id] = StudentProfile(student_id, impairment_type)
    return student_profiles[student_id]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        impairment_type = request.form.get('impairment_type')
        
        # Store in session
        session['student_id'] = student_id
        session['impairment_type'] = impairment_type
        
        # Get or create student profile
        student_profile = get_student_profile(student_id, int(impairment_type))
        
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'student_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/get_lesson')
def get_lesson():
    student_id = session.get('student_id')
    if not student_id:
        return jsonify({'error': 'Not logged in'})
    
    topic = request.args.get('topic')
    profile = get_student_profile(student_id)
    lesson = lesson_generator.generate_lesson(profile, topic)
    
    return jsonify({'lesson': lesson})

@app.route('/api/check_answer', methods=['POST'])
def check_answer():
    student_id = session.get('student_id')
    if not student_id:
        return jsonify({'error': 'Not logged in'})
    
    data = request.get_json()
    problem = data.get('problem', {})
    user_answer = data.get('answer', '')
    
    profile = get_student_profile(student_id)
    
    # Check answer and generate feedback
    feedback_data = feedback_engine.generate_feedback(problem, user_answer, profile)
    
    # Update student progress
    profile.update_progress(
        problem.get('type', ''),
        problem.get('subtype', ''),
        feedback_data['is_correct']
    )
    
    return jsonify(feedback_data)

@app.route('/api/speak', methods=['POST'])
def speak():
    data = request.get_json()
    text = data.get('text', '')
    is_equation = data.get('is_equation', False)
    
    success = speech_engine.speak(text, is_equation)
    
    return jsonify({'success': success})

@app.route('/api/get_progress')
def get_progress():
    student_id = session.get('student_id')
    if not student_id:
        return jsonify({'error': 'Not logged in'})
    
    profile = get_student_profile(student_id)
    report = feedback_engine.generate_progress_report(profile)
    
    return jsonify(report)

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs('data/profiles', exist_ok=True)
    os.makedirs('data/sessions', exist_ok=True)
    
    app.run(debug=True)