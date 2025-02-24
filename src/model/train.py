import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import load_dataset
from peft import prepare_model_for_kbit_training, LoraConfig, get_peft_model

def prepare_dataset():
    # Load your Sinhala mathematics dataset
    dataset = load_dataset("json", data_files="data/processed/math_problems.json")
    return dataset

def prepare_model():
    # Load base model
    model = AutoModelForCausalLM.from_pretrained(
        "meta-llama/Llama-3-7b",  # Replace with actual model name
        load_in_4bit=True,
        device_map="auto",
        torch_dtype=torch.float16,
    )
    
    # Configure LoRA
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    
    # Prepare model for training
    model = prepare_model_for_kbit_training(model)
    model = get_peft_model(model, lora_config)
    
    return model

def main():
    # Initialize tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        "meta-llama/Llama-3-7b",  # Replace with actual model name
        use_fast=True
    )
    tokenizer.pad_token = tokenizer.eos_token
    
    # Prepare dataset
    dataset = prepare_dataset()
    
    # Prepare model
    model = prepare_model()
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir="outputs",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        fp16=True,
        logging_steps=100,
        save_steps=500,
        eval_steps=500,
    )
    
    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["validation"],
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
    )
    
    # Start training
    trainer.train()
    
    # Save model
    trainer.save_model("final_model")

if __name__ == "__main__":
    main() 