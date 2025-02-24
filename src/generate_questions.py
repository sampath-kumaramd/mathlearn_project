from src.api.inference import MathContentGenerator
import torch
import os

def main():
    # Check if CUDA is available
    if not torch.cuda.is_available():
        print("Warning: CUDA not available. Using CPU.")
    
    # Define paths
    base_model_path = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    model_path = "./final_model"  # Changed to relative path
    
    # Check if model exists
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model not found at {model_path}. Please run training first using:\n"
            "python -m src.model.train"
        )
    
    # Initialize the model
    model = MathContentGenerator(
        model_path=model_path,
        base_model_path=base_model_path
    )
    
    # Example topics and difficulties
    topics = ["addition", "subtraction", "multiplication", "division"]
    difficulties = ["easy", "medium", "hard"]
    
    # Generate some sample problems
    for topic in topics:
        for difficulty in difficulties:
            prompt = f"""### Instruction:
                ගණිත ගැටළුව සාදන්න
                විෂය: {topic}
                අපහසුතා මට්ටම: {difficulty}

                ### Response:
                """
            # Generate problem
            generated_problem = model.generate_math_problem(prompt)
            print(f"\nTopic: {topic}, Difficulty: {difficulty}")
            print("Generated Problem:")
            print(generated_problem)
            print("-" * 50)

if __name__ == "__main__":
    main() 