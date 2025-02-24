from math_problem_generator import TrainingDataGenerator
import json

def main():
    # Initialize generator
    generator = TrainingDataGenerator()
    
    # Generate training data (reduced number for testing)
    training_data = generator.generate_training_data(num_problems=1000)
    
    # Save to JSON file
    output_file = "data/processed/math_problems.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(training_data, f, ensure_ascii=False, indent=2)
    
    print(f"Generated {len(training_data)} training examples")

if __name__ == "__main__":
    main() 