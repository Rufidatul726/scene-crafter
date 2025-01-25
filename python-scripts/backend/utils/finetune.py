import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainingArguments, Seq2SeqTrainer
from datasets import load_dataset

# Model and tokenizer
MODEL_NAME = "Salesforce/codet5-small"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

# Load dataset
dataset = load_dataset("json", data_files={"train": "train.json", "validation": "valid.json"})

# Preprocess dataset
def preprocess_data(batch):
    inputs = tokenizer(batch["prompt"], truncation=True, max_length=128, padding="max_length")
    targets = tokenizer(batch["target"], truncation=True, max_length=512, padding="max_length")
    batch["input_ids"] = inputs.input_ids
    batch["attention_mask"] = inputs.attention_mask
    batch["labels"] = targets.input_ids
    return batch

tokenized_dataset = dataset.map(preprocess_data, batched=True)

# Fine-tuning arguments
training_args = Seq2SeqTrainingArguments(
    output_dir="./codeT5-fine-tuned",
    evaluation_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    save_total_limit=2,
    predict_with_generate=True,
    logging_dir="./logs",
    logging_steps=10,
    push_to_hub=False,
)

# Trainer
trainer = Seq2SeqTrainer(
    model=model,
    tokenizer=tokenizer,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"],
)

# Train the model
trainer.train()

# Save the fine-tuned model
model.save_pretrained("./codeT5-fine-tuned")
tokenizer.save_pretrained("./codeT5-fine-tuned")
