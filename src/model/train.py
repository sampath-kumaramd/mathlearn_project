import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import load_dataset, DatasetDict
from peft import prepare_model_for_kbit_training, LoraConfig, get_peft_model

def prepare_dataset(tokenizer):
    """Load and prepare the dataset for training"""
    try:
        # Load the dataset
        dataset = load_dataset("json", 
                             data_files="data/processed/math_problems.json",
                             field="problems")
        
        def format_for_model(examples):
            """Format examples for model training"""
            texts = []
            for q, a, t, d in zip(examples['question'], examples['answer'], 
                                examples['type'], examples['difficulty']):
                # Format as instruction-following text
                text = f"""### Instruction:
ගණිත ගැටළුව විසඳන්න
විෂය: {t}
අපහසුතා මට්ටම: {d}

### Input:
{q}

### Response:
පිළිතුර: {a}
"""
                texts.append(text)
            
            # Tokenize the texts
            tokenized = tokenizer(
                texts,
                truncation=True,
                padding=True,
                max_length=512,
                return_tensors=None  # Return Python lists instead of tensors
            )
            
            return tokenized

        # Process dataset
        processed_dataset = dataset["train"].map(
            format_for_model,
            batched=True,
            remove_columns=dataset["train"].column_names,
            desc="Processing dataset"
        )
        
        # Split into train and validation
        splits = processed_dataset.train_test_split(test_size=0.1, seed=42)
        
        return DatasetDict({
            "train": splits["train"],
            "validation": splits["test"]
        })
        
    except FileNotFoundError:
        print("Error: Training data file not found. Generating sample data...")
        from src.data.generate_training_data import generate_training_dataset
        generate_training_dataset()
        # Try loading again
        return prepare_dataset(tokenizer)

def prepare_model():
    # Load base model
    model = AutoModelForCausalLM.from_pretrained(
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0",  # Changed to open-source model
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
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        use_fast=True
    )
    tokenizer.pad_token = tokenizer.eos_token
    
    # Prepare dataset with tokenizer
    dataset = prepare_dataset(tokenizer)
    
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
        remove_unused_columns=True,
        prediction_loss_only=True,
        logging_dir="logs",
        save_total_limit=2
    )
    
    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["validation"],
        data_collator=DataCollatorForLanguageModeling(
            tokenizer=tokenizer,
            mlm=False
        )
    )
    
    # Start training
    trainer.train()
    
    # Save model
    trainer.save_model("final_model")

def run_training():
    # Check GPU availability
    if not torch.cuda.is_available():
        raise RuntimeError("Training requires a GPU")
    
    # Run training
    main()

if __name__ == "__main__":
    run_training() 