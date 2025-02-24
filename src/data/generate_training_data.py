import os
import json
from ..cultural.problem_generator import CulturalProblemGenerator

def generate_training_dataset(num_problems=1000):
    """Generate training dataset for math problems"""
    
    # Initialize problem generator
    generator = CulturalProblemGenerator()
    
    # Generate problems
    problems = []
    topics = ["addition", "subtraction", "multiplication", "division"]
    difficulties = range(1, 11)
    
    for topic in topics:
        for difficulty in difficulties:
            for _ in range(num_problems // (len(topics) * len(difficulties))):
                problem = generator.generate_problem(topic, difficulty)
                if problem:
                    problems.append(problem)
    
    # Ensure output directory exists
    os.makedirs("data/processed", exist_ok=True)
    
    # Save to JSON file
    output_file = "data/processed/math_problems.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({"problems": problems}, f, ensure_ascii=False, indent=2)
    
    print(f"Generated {len(problems)} problems and saved to {output_file}")

if __name__ == "__main__":
    generate_training_dataset() 