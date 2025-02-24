# src/feedback/feedback_engine.py

import random
import json
import os
import datetime

class FeedbackEngine:
    def __init__(self, speech_engine, language='si'):
        self.speech_engine = speech_engine
        self.language = language
        self.error_patterns = self._load_error_patterns()
        self.feedback_templates = self._load_feedback_templates()
    
    def _load_error_patterns(self):
        """Load common error patterns in mathematics"""
        try:
            file_path = os.path.join(os.path.dirname(__file__), 
                                   '../data/error_patterns.json')
            
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            else:
                # Default error patterns if file doesn't exist
                return {
                    "sign_reversal": {
                        "pattern": "opposite_sign_result",
                        "explanation": "ඔබ සලකුණු වැරදියට භාවිතා කර ඇත. ධන සහ ඍණ සලකුණු පිළිබඳව ප්‍රවේශම් වන්න."
                    },
                    "calculation_error": {
                        "pattern": "incorrect_arithmetic",
                        "explanation": "ගණනය කිරීමේ දෝෂයක් ඇත. කරුණාකර ඔබේ සංඛ්‍යා නැවත පරීක්ෂා කරන්න."
                    },
                    "decimal_misalignment": {
                        "pattern": "decimal_misplaced",
                        "explanation": "දශම ස්ථානය වැරදියි. දශම ස්ථාන ගැලපීම පිළිබඳව ප්‍රවේශම් වන්න."
                    }
                }
        except Exception as e:
            print(f"Error loading error patterns: {e}")
            return {}
    
    def _load_feedback_templates(self):
        """Load feedback templates"""
        try:
            file_path = os.path.join(os.path.dirname(__file__), 
                                   '../data/feedback_templates.json')
            
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            else:
                # Default templates if file doesn't exist
                return {
                    "correct": [
                        "නිවැරදියි! ඔබ හොඳ වැඩක් කළා.",
                        "එය හරි! ඔබ දැන් මෙම සංකල්පය තේරුම් ගනී.",
                        "නියමයි! ඔබ නිවැරදිව ගණනය කර ඇත."
                    ],
                    "incorrect": [
                        "එය හරි නැත. නැවත උත්සාහ කරන්න.",
                        "වැරදියි. ඔබේ පිළිතුර {answer} විය යුතුයි.",
                        "ඔබේ පිළිතුර වැරදියි. මේ ගැන නැවත සිතන්න."
                    ],
                    "hint": [
                        "ඔබ මෙම ගැටලුව විසඳීමට {concept} භාවිතා කළ යුතුයි.",
                        "පළමුව {step_1} සිදු කරන්න, ඉන්පසු {step_2}.",
                        "මෙම ගැටලුව සඳහා {formula} සූත්‍රය සිහිපත් කරන්න."
                    ],
                    "encouragement": [
                        "ඔබට මෙය කළ හැකිය! නැවත උත්සාහ කරන්න.",
                        "මෙම සංකල්පය අපහසු විය හැකිය. ඉවසීමෙන් නැවත උත්සාහ කරන්න.",
                        "වැරදීම් ඉගෙනීමේ ක්‍රියාවලියේ කොටසක්. නැවත උත්සාහ කරන්න."
                    ]
                }
        except Exception as e:
            print(f"Error loading feedback templates: {e}")
            return {}
    
    def analyze_error(self, problem, user_answer):
        """Analyze the type of error in the student's answer"""
        # Extract problem data
        problem_type = problem.get("type", "")
        correct_answer = problem.get("answer", "")
        
        # Basic error analysis
        try:
            user_value = float(user_answer)
            correct_value = float(correct_answer)
            
            # Check for sign reversal
            if user_value == -correct_value:
                return "sign_reversal"
            
            # Check for decimal misalignment
            if abs(user_value / correct_value) % 10 == 0 or abs(correct_value / user_value) % 10 == 0:
                return "decimal_misalignment"
            
            # Check for off-by-one errors
            if abs(user_value - correct_value) == 1:
                return "off_by_one"
            
            # Default to general calculation error
            return "calculation_error"
        except:
            # If conversion to float fails, it's a format error
            return "format_error"
    
    def generate_feedback(self, problem, user_answer, student_profile=None):
        """Generate appropriate feedback based on answer and profile"""
        correct_answer = problem.get("answer", "")
        is_correct = str(user_answer).strip() == str(correct_answer).strip()
        
        feedback_data = {
            "is_correct": is_correct,
            "correct_answer": correct_answer,
            "feedback_text": "",
            "explanation": "",
            "next_steps": []
        }
        
        if is_correct:
            # Positive feedback for correct answer
            feedback_data["feedback_text"] = random.choice(
                self.feedback_templates.get("correct", ["නිවැරදියි!"]))
        else:
            # Error analysis and specific feedback
            error_type = self.analyze_error(problem, user_answer)
            
            # Get error explanation if available
            if error_type in self.error_patterns:
                explanation = self.error_patterns[error_type].get("explanation", "")
                feedback_data["explanation"] = explanation
            
            # Basic incorrect feedback
            templates = self.feedback_templates.get("incorrect", ["වැරදියි."])
            selected_template = random.choice(templates)
            feedback_data["feedback_text"] = selected_template.replace("{answer}", str(correct_answer))
            
            # Add encouragement based on student profile if available
            if student_profile:
                # Check if student is struggling with this topic
                topic = problem.get("type", "")
                proficiency = student_profile.get_proficiency_level(topic)
                
                if proficiency < 3:  # Low proficiency
                    encouragement = random.choice(
                        self.feedback_templates.get("encouragement", ["නැවත උත්සාහ කරන්න."]))
                    feedback_data["feedback_text"] += " " + encouragement
            
            # Suggest next steps
            feedback_data["next_steps"] = [
                "ගැටලුව නැවත කියවන්න.",
                "පියවරෙන් පියවර විසඳුම සඳහා උත්සාහ කරන්න.",
                "සමාන ගැටලු සඳහා උදාහරණ බලන්න."
            ]
        
        return feedback_data
    
    def deliver_feedback(self, feedback_data):
        """Deliver feedback via speech"""
        # Combine feedback text and explanation
        speech_text = feedback_data["feedback_text"]
        
        if not feedback_data["is_correct"] and feedback_data["explanation"]:
            speech_text += " " + feedback_data["explanation"]
        
        # Speak the feedback
        self.speech_engine.speak(speech_text)
        
        return True
    
    def detect_emotion(self, audio_data):
        """Detect student emotion from audio (placeholder)"""
        # This would be implemented with MediaPipe or another audio analysis
        
        
    def detect_emotion(self, audio_data):
        """Detect student emotion from audio input"""
        # This would be implemented with MediaPipe in a full implementation
        # For now, providing a placeholder implementation
        
        # Assuming audio_data contains metrics about speech patterns
        # such as speaking rate, pitch variations, and pauses
        
        # Simplified analysis (would be ML-based in full implementation)
        if "extended_pauses" in audio_data and audio_data["extended_pauses"] > 3:
            return "frustrated"
        elif "pitch_variations" in audio_data and audio_data["pitch_variations"] > 0.8:
            return "excited"
        elif "speaking_rate" in audio_data and audio_data["speaking_rate"] < 0.7:
            return "confused"
        else:
            return "neutral"
    
    def adapt_pacing(self, student_profile, detected_emotion):
        """Adjust learning pace based on emotion and profile"""
        impairment_type = student_profile.impairment_type if student_profile else 1
        
        pacing_adjustments = {
            "neutral": {
                "explanation_depth": "normal",
                "speech_rate": 1.0,
                "additional_examples": False
            },
            "confused": {
                "explanation_depth": "detailed",
                "speech_rate": 0.8,
                "additional_examples": True
            },
            "frustrated": {
                "explanation_depth": "simplified",
                "speech_rate": 0.9,
                "additional_examples": True
            },
            "excited": {
                "explanation_depth": "advanced",
                "speech_rate": 1.1,
                "additional_examples": False
            }
        }
        
        # Get base adjustments for detected emotion
        adjustments = pacing_adjustments.get(detected_emotion, pacing_adjustments["neutral"])
        
        # Further customize based on impairment type
        if impairment_type == 1:  # Congenital blindness
            adjustments["explanation_style"] = "audio_descriptive"
        elif impairment_type == 2:  # Acquired blindness
            adjustments["explanation_style"] = "spatial_reference"
        elif impairment_type == 3:  # Low vision
            adjustments["explanation_style"] = "high_contrast_audio"
        
        return adjustments
    
    def generate_progress_report(self, student_profile, time_period="biweekly"):
        """Generate a progress report for the student"""
        # This would analyze the student's performance history
        # and generate a comprehensive report
        
        # For a basic implementation, let's create a simple report
        report = {
            "student_id": student_profile.student_id,
            "report_date": datetime.datetime.now().isoformat(),
            "period": time_period,
            "overall_progress": {},
            "topic_progress": {},
            "recommendations": []
        }
        
        # Calculate overall progress
        overall_level = student_profile.get_proficiency_level()
        report["overall_progress"] = {
            "current_level": overall_level,
            "improvement": 0  # Would be calculated from historical data
        }
        
        # Topic-specific progress
        for topic, level in student_profile.topic_progress.items():
            # This would include historical comparison in full implementation
            report["topic_progress"][topic] = {
                "current_level": level,
                "improvement": 0  # Placeholder
            }
        
        # Generate recommendations
        learning_path = student_profile.get_learning_path()
        for path_item in learning_path:
            report["recommendations"].append({
                "topic": path_item["topic"],
                "reason": f"Current proficiency is {path_item['current_level']}/10",
                "suggested_exercises": ["Basic", "Intermediate", "Advanced"]
                                      [min(int(path_item["current_level"]/3), 2)]
            })
        
        return report