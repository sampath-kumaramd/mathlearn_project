# src/learning/student_profile.py

import json
import os
import datetime
from collections import defaultdict

class StudentProfile:
    def __init__(self, student_id, impairment_type=1):
        """
        Initialize student profile
        
        impairment_type:
        1 - Congenital blindness
        2 - Acquired blindness
        3 - Low vision
        """
        self.student_id = student_id
        self.impairment_type = impairment_type
        
        # Initialize learning progress
        self.topic_progress = defaultdict(lambda: 1)
        self.performance_history = []
        self.learning_objectives = self._initialize_learning_objectives()
        
        # Load existing profile if available
        self._load_profile()
    
    def _initialize_learning_objectives(self):
        """Initialize the 42 learning objectives from curriculum"""
        # This would ideally be loaded from a more comprehensive dataset
        # Here's a simplified version with just a few objectives
        return {
            "algebra": {
                "linear_equations": 1,
                "quadratic_equations": 1,
                "polynomials": 1
            },
            "geometry": {
                "triangles": 1,
                "circles": 1,
                "angles": 1
            },
            "arithmetic": {
                "fractions": 1,
                "decimals": 1,
                "percentages": 1
            }
        }
    
    def _load_profile(self):
        """Load existing profile if available"""
        profile_path = os.path.join(os.path.dirname(__file__), 
                               f'../data/profiles/{self.student_id}.json')
        
        if os.path.exists(profile_path):
            try:
                with open(profile_path, 'r', encoding='utf-8') as file:
                    profile_data = json.load(file)
                    
                    # Load impairment type
                    self.impairment_type = profile_data.get('impairment_type', 1)
                    
                    # Load topic progress
                    for topic, level in profile_data.get('topic_progress', {}).items():
                        self.topic_progress[topic] = level
                    
                    # Load performance history
                    self.performance_history = profile_data.get('performance_history', [])
                    
                    # Load learning objectives
                    objectives = profile_data.get('learning_objectives', {})
                    for category, objectives_dict in objectives.items():
                        if category in self.learning_objectives:
                            for objective, level in objectives_dict.items():
                                if objective in self.learning_objectives[category]:
                                    self.learning_objectives[category][objective] = level
            except Exception as e:
                print(f"Error loading profile: {e}")
    
    def save_profile(self):
        """Save student profile to file"""
        # Ensure directory exists
        os.makedirs(os.path.join(os.path.dirname(__file__), '../data/profiles'), 
                   exist_ok=True)
        
        profile_path = os.path.join(os.path.dirname(__file__), 
                               f'../data/profiles/{self.student_id}.json')
        
        try:
            profile_data = {
                'student_id': self.student_id,
                'impairment_type': self.impairment_type,
                'topic_progress': dict(self.topic_progress),
                'performance_history': self.performance_history,
                'learning_objectives': self.learning_objectives,
                'last_updated': datetime.datetime.now().isoformat()
            }
            
            with open(profile_path, 'w', encoding='utf-8') as file:
                json.dump(profile_data, file, indent=2, ensure_ascii=False)
                
            return True
        except Exception as e:
            print(f"Error saving profile: {e}")
            return False
    
    def update_progress(self, topic, subtopic, is_correct, response_time=None):
        """Update student progress based on performance"""
        # Record performance
        performance_record = {
            'timestamp': datetime.datetime.now().isoformat(),
            'topic': topic,
            'subtopic': subtopic,
            'is_correct': is_correct,
            'response_time': response_time
        }
        
        self.performance_history.append(performance_record)
        
        # Update topic progress
        if is_correct:
            self.topic_progress[topic] = min(10, self.topic_progress[topic] + 0.2)
        else:
            self.topic_progress[topic] = max(1, self.topic_progress[topic] - 0.1)
        
        # Update specific learning objective if applicable
        if topic in self.learning_objectives and subtopic in self.learning_objectives[topic]:
            if is_correct:
                self.learning_objectives[topic][subtopic] = min(
                    10, self.learning_objectives[topic][subtopic] + 0.2)
            else:
                self.learning_objectives[topic][subtopic] = max(
                    1, self.learning_objectives[topic][subtopic] - 0.1)
        
        # Save the updated profile
        self.save_profile()
    
    def get_proficiency_level(self, topic=None, subtopic=None):
        """Get student's proficiency level overall or for specific topic"""
        if topic and subtopic and topic in self.learning_objectives:
            if subtopic in self.learning_objectives[topic]:
                return self.learning_objectives[topic][subtopic]
            return 1
        
        if topic:
            return self.topic_progress.get(topic, 1)
        
        # Overall proficiency is average of all topics
        if len(self.topic_progress) > 0:
            return sum(self.topic_progress.values()) / len(self.topic_progress)
        return 1
    
    def get_learning_path(self):
        """Generate personalized learning path based on profile"""
        # Identify weakest areas
        weak_topics = []
        
        # Check topic proficiency
        for topic, level in self.topic_progress.items():
            if level < 5:  # Below average proficiency
                weak_topics.append((topic, level))
        
        # If no weak topics found, look at specific learning objectives
        if not weak_topics:
            for category, objectives in self.learning_objectives.items():
                for objective, level in objectives.items():
                    if level < 5:  # Below average proficiency
                        weak_topics.append((f"{category}_{objective}", level))
        
        # Sort by proficiency level (ascending)
        weak_topics.sort(key=lambda x: x[1])
        
        # Create learning path focusing on weakest areas first
        learning_path = [
            {
                "topic": topic_name,
                "current_level": level,
                "target_level": min(10, level + 2),
                "priority": index + 1
            }
            for index, (topic_name, level) in enumerate(weak_topics[:3])
        ]
        
        return learning_path
    
    def get_learning_style(self):
        """Determine optimal learning style based on impairment type"""
        if self.impairment_type == 1:  # Congenital blindness
            return {
                "interaction_mode": "audio_centric",
                "feedback_style": "descriptive",
                "pacing": "moderate",
                "explanation_depth": "detailed"
            }
        elif self.impairment_type == 2:  # Acquired blindness
            return {
                "interaction_mode": "audio_with_spatial_references",
                "feedback_style": "comparative",
                "pacing": "adjustable",
                "explanation_depth": "graduated"
            }
        elif self.impairment_type == 3:  # Low vision
            return {
                "interaction_mode": "audio_with_high_contrast",
                "feedback_style": "highlight_based",
                "pacing": "user_controlled",
                "explanation_depth": "concise"
            }
        else:
            # Default style
            return {
                "interaction_mode": "audio_centric",
                "feedback_style": "descriptive",
                "pacing": "moderate",
                "explanation_depth": "detailed"
            }