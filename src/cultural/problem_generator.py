# src/cultural/problem_generator.py

import random
import json
import os
from datetime import datetime

class CulturalProblemGenerator:
    def __init__(self):
        self.contexts = {
            "rural": ["ගොවිපල", "කුඹුර", "වත්ත", "ගම්මානය"],
            "urban": ["පාසල", "සාප්පුව", "බස් රථය", "කඩය"]
        }
        
    def generate_problem(self, topic, difficulty):
        """Generate a culturally relevant math problem"""
        context_type = "rural" if random.random() < 0.6 else "urban"  # 60:40 ratio
        context = random.choice(self.contexts[context_type])
        
        if topic == "addition":
            return self._generate_addition_problem(context, difficulty)
        elif topic == "subtraction":
            return self._generate_subtraction_problem(context, difficulty)
        elif topic == "multiplication":
            return self._generate_multiplication_problem(context, difficulty)
        elif topic == "division":
            return self._generate_division_problem(context, difficulty)
        elif topic == "probability":
            return self._generate_probability_problem(context, difficulty)
            
        return None
        
    def _generate_addition_problem(self, context, difficulty):
        """Generate addition problem with cultural context"""
        # Generate numbers based on difficulty
        num1 = random.randint(1, difficulty * 10)
        num2 = random.randint(1, difficulty * 10)
        
        question = f"{context}ට පළමුව {num1} ක් සහ පසුව {num2} ක් එකතු විය. මුළු එකතුව කීයද?"
        
        return {
            "type": "addition",
            "difficulty": difficulty,
            "question": question,
            "answer": num1 + num2,
            "context_type": "rural" if context in self.contexts["rural"] else "urban"
        }
        
    def _generate_subtraction_problem(self, context, difficulty):
        """Generate subtraction problem with cultural context"""
        total = random.randint(difficulty * 10, difficulty * 20)
        subtract = random.randint(1, total)
        
        question = f"{context}ේ මුලින් {total} ක් තිබුණි. පසුව {subtract} ක් ඉවත් කළ විට ඉතිරි වූයේ කීයද?"
        
        return {
            "type": "subtraction",
            "difficulty": difficulty,
            "question": question,
            "answer": total - subtract,
            "context_type": "rural" if context in self.contexts["rural"] else "urban"
        }
    
    def _generate_multiplication_problem(self, context, difficulty):
        """Generate multiplication problem with cultural context"""
        # Generate numbers based on difficulty
        num1 = random.randint(1, difficulty * 5)
        num2 = random.randint(1, difficulty * 5)
        
        question = f"{context}ේ එක් පේළියක {num1} බැගින් පේළි {num2} ක් ඇත. මුළු ගණන කීයද?"
        
        return {
            "type": "multiplication",
            "difficulty": difficulty,
            "question": question,
            "answer": num1 * num2,
            "context_type": "rural" if context in self.contexts["rural"] else "urban"
        }
    
    def _generate_division_problem(self, context, difficulty):
        """Generate division problem with cultural context"""
        # Generate numbers based on difficulty
        divisor = random.randint(2, difficulty * 2)
        quotient = random.randint(1, difficulty * 5)
        total = divisor * quotient
        
        question = f"{context}ේ {total} ක් {divisor} දෙනෙකු අතර සමව බෙදිය යුතුය. එක් අයෙකුට කීයක් බැගින් හිමිවේද?"
        
        return {
            "type": "division",
            "difficulty": difficulty,
            "question": question,
            "answer": quotient,
            "context_type": "rural" if context in self.contexts["rural"] else "urban"
        }
    
    def _generate_probability_problem(self, context, difficulty):
        """Generate probability problem with cultural context"""
        # Generate numbers based on difficulty
        total_items = random.randint(difficulty * 5, difficulty * 10)
        target_items = random.randint(1, total_items)
        
        # Create culturally relevant probability questions
        question_types = [
            # Type 1: Simple probability with fruits/vegetables
            lambda: f"{context}ේ {total_items} ක් අතරින් {target_items} ක් ගෙඩි ඇත. අහඹු ලෙස එක් ගෙඩියක් තෝරා ගැනීමේ සම්භාවිතාව කීයද?",
            
            # Type 2: Probability with students
            lambda: f"{context}ේ සිටින {total_items} දෙනා අතරින් {target_items} දෙනෙක් ශිෂ්‍යයන් වේ. අහඹු ලෙස කෙනෙකු තෝරා ගැනීමේදී ඔහු/ඇය ශිෂ්‍යයෙකු වීමේ සම්භාවිතාව කීයද?",
            
            # Type 3: Weather-based probability
            lambda: f"පසුගිය {total_items} දිනයන් අතරින් {target_items} දිනයන්හි වැසි ලැබිණි. ඊළඟ දිනයේ වැසි ලැබීමේ සම්භාවිතාව කීයද?"
        ]
        
        # Select random question type
        question = random.choice(question_types)()
        
        # Calculate probability as a fraction
        answer = f"{target_items}/{total_items}"
        
        return {
            "type": "probability",
            "difficulty": difficulty,
            "question": question,
            "answer": answer,
            "context_type": "rural" if context in self.contexts["rural"] else "urban",
            "total_items": total_items,
            "target_items": target_items
        }

def generate_training_dataset(num_problems=1000):
    """Generate training dataset for math problems"""
    
    # Initialize problem generator
    problem_generator = CulturalProblemGenerator()
    
    # Topics and difficulties to generate problems for
    topics = ["addition", "subtraction", "multiplication", "division"]
    difficulties = range(1, 11)  # 1-10 difficulty levels
    
    # Generate problems
    problems = []
    for topic in topics:
        for difficulty in difficulties:
            # Generate multiple problems per difficulty level
            for _ in range(num_problems // (len(topics) * len(difficulties))):
                problem = problem_generator.generate_problem(topic, difficulty)
                if problem:
                    problems.append({
                        "text": problem["question"],
                        "answer": str(problem["answer"]),
                        "type": problem["type"],
                        "difficulty": problem["difficulty"],
                        "context_type": problem["context_type"]
                    })
    
    # Ensure output directory exists
    os.makedirs("data/processed", exist_ok=True)
    
    # Save to JSON file
    output_file = "data/processed/math_problems.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({"problems": problems}, f, ensure_ascii=False, indent=2)
    
    print(f"Generated {len(problems)} problems and saved to {output_file}")

if __name__ == "__main__":
    generate_training_dataset()