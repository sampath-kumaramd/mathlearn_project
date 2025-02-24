import json
import random
from tqdm import tqdm
from ..cultural.problem_generator import CulturalProblemGenerator

class TrainingDataGenerator:
    def __init__(self):
        self.problem_generator = CulturalProblemGenerator()
        self.topics = ["addition", "subtraction", "multiplication", "division", "probability"]
        self.difficulty_levels = range(1, 11)  # 1-10 difficulty levels
        
    def generate_training_data(self, num_problems=50000):
        """Generate training data for Llama 3 fine-tuning"""
        training_data = []
        
        for _ in tqdm(range(num_problems)):
            # Randomly select topic and difficulty
            topic = random.choice(self.topics)
            difficulty = random.choice(self.difficulty_levels)
            
            # Generate problem
            problem = self.problem_generator.generate_problem(topic, difficulty)
            
            # Format for training
            training_example = self._format_for_training(problem)
            training_data.append(training_example)
        
        return training_data
    
    def _format_for_training(self, problem):
        """Format problem for Llama 3 training"""
        instruction = "ගණිත ගැටළුව විසඳන්න:"
        context = f"විෂය: {problem['type']}\nඅපහසුතා මට්ටම: {problem['difficulty']}"
        
        # Format input-output pair
        formatted = {
            "instruction": instruction,
            "input": f"{context}\n\nප්‍රශ්නය: {problem['question']}",
            "output": f"පිළිතුර: {problem['answer']}\n\nවිසඳුම:\n{self._generate_solution_steps(problem)}"
        }
        
        return formatted
    
    def _generate_solution_steps(self, problem):
        """Generate solution steps in Sinhala"""
        if problem['type'] == "addition":
            numbers = self._extract_numbers(problem['question'])
            steps = [
                f"1. දී ඇති සංඛ්‍යා හඳුනා ගනිමු: {numbers[0]} සහ {numbers[1]}",
                f"2. සංඛ්‍යා එකතු කරමු: {numbers[0]} + {numbers[1]} = {problem['answer']}",
                f"3. අවසාන පිළිතුර: {problem['answer']}"
            ]
            return "\n".join(steps)
        elif problem['type'] == "probability":
            total = problem.get('total_items', 0)
            target = problem.get('target_items', 0)
            steps = [
                f"1. මුළු සංඛ්‍යාව හඳුනා ගනිමු: {total}",
                f"2. අවශ්‍ය සිදුවීම් ගණන හඳුනා ගනිමු: {target}",
                f"3. සම්භාවිතාව ගණනය කරමු: {target}/{total}",
                f"4. අවසාන පිළිතුර: {problem['answer']}"
            ]
            return "\n".join(steps)
        return "විසඳුම පියවරෙන් පියවර"
    
    def _extract_numbers(self, text):
        """Extract numbers from problem text"""
        import re
        return [int(num) for num in re.findall(r'\d+', text)]

def main():
    # Initialize generator
    generator = TrainingDataGenerator()
    
    # Generate training data
    training_data = generator.generate_training_data(num_problems=50000)
    
    # Save to JSON file
    output_file = "data/training/math_problems_sinhala.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(training_data, f, ensure_ascii=False, indent=2)
    
    print(f"Generated {len(training_data)} training examples")

if __name__ == "__main__":
    main() 