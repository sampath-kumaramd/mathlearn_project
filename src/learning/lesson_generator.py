# src/learning/lesson_generator.py

import random
from ..cultural.problem_generator import CulturalProblemGenerator

class AdaptiveLessonGenerator:
    def __init__(self):
        self.problem_generator = CulturalProblemGenerator()
        
    def generate_lesson(self, student_profile, focus_topic=None):
        """Generate a personalized lesson based on student profile"""
        # Get learning path if no focus topic specified
        if not focus_topic:
            learning_path = student_profile.get_learning_path()
            if learning_path:
                focus_topic = learning_path[0]["topic"]
            else:
                focus_topic = "addition"  # Default
        
        # Get current proficiency level
        current_level = student_profile.get_proficiency_level(focus_topic)
        difficulty = max(1, min(10, int(current_level)))
        
        # Get optimal learning style
        learning_style = student_profile.get_learning_style()
        
        # Structure the lesson
        lesson = {
            "topic": focus_topic,
            "difficulty": difficulty,
            "learning_style": learning_style,
            "introduction": self._generate_introduction(focus_topic, difficulty),
            "examples": self._generate_examples(focus_topic, difficulty, 2),
            "problems": self._generate_problems(focus_topic, difficulty, 5),
            "summary": self._generate_summary(focus_topic)
        }
        
        return lesson
    
    def _generate_introduction(self, topic, difficulty):
        """Generate topic introduction based on difficulty level"""
        # This would be more comprehensive in a full implementation
        topics_intro = {
            "addition": "එකතු කිරීම යනු දෙකක් හෝ ඊට වැඩි ගණනක් එකතු කිරීමේ ක්‍රියාවලියයි.",
            "subtraction": "අඩු කිරීම යනු එක් අගයකින් තවත් අගයක් ඉවත් කිරීමේ ක්‍රියාවලියයි.",
            "multiplication": "ගුණ කිරීම යනු සංඛ්‍යාවක් කිහිප වතාවක් එකතු කිරීමේ කෙටි ක්‍රමයයි.",
            "division": "බෙදීම යනු ප්‍රමාණයක් කොටස් වලට බෙදීමේ ක්‍රියාවලියයි."
        }
        
        return topics_intro.get(topic, f"{topic} පිළිබඳ හැඳින්වීම")
    
    def _generate_examples(self, topic, difficulty, count=2):
        """Generate worked examples of increasing complexity"""
        examples = []
        
        # Start with simpler examples than the target difficulty
        start_difficulty = max(1, difficulty - 1)
        
        for i in range(count):
            # Gradually increase difficulty
            example_difficulty = min(10, start_difficulty + i)
            
            # Generate a problem
            problem = self.problem_generator.generate_problem(topic, example_difficulty)
            
            # Add worked solution steps
            problem["solution_steps"] = self._generate_solution_steps(problem)
            
            examples.append(problem)
        
        return examples
    
    def _generate_problems(self, topic, difficulty, count=5):
        """Generate practice problems for the lesson"""
        problems = []
        
        for i in range(count):
            # Vary difficulty slightly around the target level
            problem_difficulty = max(1, min(10, difficulty + random.randint(-1, 1)))
            
            problem = self.problem_generator.generate_problem(topic, problem_difficulty)
            problems.append(problem)
        
        return problems
    
    def _generate_solution_steps(self, problem):
        """Generate step-by-step solution for a problem"""
        # This would be more sophisticated in a full implementation
        # For now, providing a simple implementation
        
        steps = []
        problem_type = problem.get("type", "")
        
        if problem_type == "addition":
            a, b = self._extract_numbers_from_question(problem["question"])
            steps = [
                f"පළමුව, අපට එකතු කිරීමට ඇති සංඛ්‍යා හඳුනාගනිමු: {a} සහ {b}",
                f"දැන් අපි එම සංඛ්‍යා එකතු කරමු: {a} + {b}",
                f"අවසාන පිළිතුර: {a + b}"
            ]
        elif problem_type == "subtraction":
            # Similar implementation for subtraction
            pass
        
        return steps
    
    def _extract_numbers_from_question(self, question):
        """Extract numerical values from question text"""
        # This is a simplified implementation
        # A more robust solution would use NLP techniques
        import re
        
        numbers = re.findall(r'\d+', question)
        if len(numbers) >= 2:
            return int(numbers[0]), int(numbers[1])
        return 0, 0
    
    def _generate_summary(self, topic):
        """Generate a summary of key points for the topic"""
        # This would be more comprehensive in a full implementation
        topics_summary = {
            "addition": "එකතු කිරීමේදී, ඔබ දෙකක් හෝ වැඩි ගණනක් සංඛ්‍යා එකතු කරන අතර අවසාන එකතුව ලබා ගනී.",
            "subtraction": "අඩු කිරීමේදී, ඔබ එක් සංඛ්‍යාවකින් තවත් සංඛ්‍යාවක් අඩු කරයි.",
            "multiplication": "ගුණ කිරීමේදී, ඔබ සංඛ්‍යාවක් වෙනත් සංඛ්‍යාවකින් වැඩි කරයි.",
            "division": "බෙදීමේදී, ඔබ සංඛ්‍යාවක් සමාන කොටස් වලට බෙදයි."
        }
        
        return topics_summary.get(topic, f"{topic} පිළිබඳ සාරාංශය")