import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

class MathContentGenerator:
    def __init__(self, model_path, base_model_path):
        self.tokenizer = AutoTokenizer.from_pretrained(base_model_path)
        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_path,
            load_in_4bit=True,
            device_map="auto",
            torch_dtype=torch.float16
        )
        self.model = PeftModel.from_pretrained(base_model, model_path)
        
    def generate_math_problem(self, prompt, max_length=512):
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        
        outputs = self.model.generate(
            **inputs,
            max_length=max_length,
            num_return_sequences=1,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )
        
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def generate_explanation(self, problem, difficulty_level="medium"):
        prompt = f"""Problem: {problem}
Difficulty: {difficulty_level}
Explanation in Sinhala:"""
        
        return self.generate_math_problem(prompt) 