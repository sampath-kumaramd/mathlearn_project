# src/cultural/problem_generator.py

import random
import json
import os
from datetime import datetime

class CulturalProblemGenerator:
    def __init__(self):
        # Load cultural contexts
        self.contexts = self._load_contexts()
        self.rural_urban_ratio = 0.6  # 60% rural as per requirements
        
    def _load_contexts(self):
        """Load cultural contexts for problem generation"""
        try:
            file_path = os.path.join(os.path.dirname(__file__), 
                                   '../data/cultural_contexts.json')
            
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            else:
                # Default contexts if file doesn't exist
                return {
                    "rural": [
                        "farming", "agriculture", "irrigation", "harvest",
                        "fishing", "village", "temple"
                    ],
                    "urban": [
                        "transportation", "building", "shopping", "school",
                        "office", "factory"
                    ],
                    "festivals": [
                        {"name": "Poson Poya", "month": 6},
                        {"name": "Vesak", "month": 5},
                        {"name": "Sinhala and Tamil New Year", "month": 4},
                        {"name": "Thai Pongal", "month": 1}
                    ],
                    "agricultural": [
                        "paddy field", "tea plantation", "coconut grove",
                        "vegetable garden", "irrigation tank"
                    ]
                }
        except Exception as e:
            print(f"Error loading cultural contexts: {e}")
            return {}
    
    def generate_problem(self, problem_type, difficulty=1):
        """Generate a culturally contextualized math problem"""
        # Determine if rural or urban context based on ratio
        context_type = "rural" if random.random() < self.rural_urban_ratio else "urban"
        
        # Check if it's festival season for probability problems
        current_month = datetime.now().month
        festival_context = None
        for festival in self.contexts.get("festivals", []):
            if festival["month"] == current_month:
                festival_context = festival["name"]
                break
        
        # Generate problem based on type
        if problem_type == "addition":
            return self._generate_addition_problem(context_type, difficulty, festival_context)
        elif problem_type == "subtraction":
            return self._generate_subtraction_problem(context_type, difficulty, festival_context)
        elif problem_type == "multiplication":
            return self._generate_multiplication_problem(context_type, difficulty, festival_context)
        elif problem_type == "division":
            return self._generate_division_problem(context_type, difficulty, festival_context)
        elif problem_type == "probability":
            return self._generate_probability_problem(context_type, difficulty, festival_context)
        else:
            return {"error": "Unknown problem type"}
    
    def _generate_addition_problem(self, context_type, difficulty, festival_context):
        """Generate addition problem with cultural context"""
        # Scale difficulty (1-10)
        max_num = 10 * difficulty
        
        a = random.randint(1, max_num)
        b = random.randint(1, max_num)
        answer = a + b
        
        # Context templates
        templates = {
            "rural": [
                f"ගොවියෙක් මුලින් කිලෝග්‍රෑම් {a} ක් සහ පසුව කිලෝග්‍රෑම් {b} ක් වී අස්වනු ලබා ගත්තේය. ඔහු මුළු වශයෙන් කොපමණ වී ප්‍රමාණයක් ලබා ගත්තේද?",
                f"ගම්මානයේ ළමයින් {a} දෙනෙක් සහ වැඩිහිටියන් {b} දෙනෙක් පන්සලට ගියහ. පන්සලට ගිය මුළු ජන ගණන කීයද?"
            ],
            "urban": [
                f"බස් රථයේ මුලින් මගීන් {a} දෙනෙක් සිටි අතර, ඊළඟ නැවතුමේදී තවත් මගීන් {b} දෙනෙක් නැග්ගහ. දැන් බස් රථයේ සිටින මුළු මගීන් ගණන කීයද?",
                f"සාප්පුවේ රුපියල් {a} ක් වටිනා පොතක් සහ රුපියල් {b} ක් වටිනා පැන්සලක් මිලදී ගතී. ඇය මුළු වශයෙන් කොපමණ මුදලක් වියදම් කළාද?"
            ]
        }
        
        # Select template
        if festival_context and random.random() < 0.3:  # 30% chance for festival context
            question = f"{festival_context} සමයේදී ගමේ වැසියන් කුඩා පහන් {a} ක් සහ විශාල පහන් {b} ක් දැල්වූහ. ඔවුන් මුළු වශයෙන් කොපමණ පහන් ගණනක් දැල්වූවාද?"
        else:
            templates_list = templates.get(context_type, templates["rural"])
            question = random.choice(templates_list)
        
        return {
            "question": question,
            "answer": answer,
            "type": "addition",
            "difficulty": difficulty,
            "context_type": context_type,
            "festival_context": festival_context
        }
    
    # Additional methods for other problem types would follow similar pattern
    def _generate_subtraction_problem(self, context_type, difficulty, festival_context):
        # Implementation for subtraction problems
        pass
    
    def _generate_multiplication_problem(self, context_type, difficulty, festival_context):
        # Implementation for multiplication problems
        pass
    
    def _generate_division_problem(self, context_type, difficulty, festival_context):
        # Implementation for division problems
        pass
    
    def _generate_probability_problem(self, context_type, difficulty, festival_context):
        # Implementation for probability problems with cultural relevance
        pass