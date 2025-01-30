import json
import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, TrainingArguments, Trainer, EarlyStoppingCallback, DataCollatorForSeq2Seq
from sklearn.model_selection import train_test_split
from datasets import Dataset

from utils.preprocess import preprocess_data, preprocess_function

def train():
    base_dir = os.path.dirname(os.path.abspath(__file__))  
    back_dir = os.path.normpath(base_dir + os.sep + os.pardir)
    print(back_dir)
    train_file_dir = os.path.join(back_dir, "files", "train_files")
    log_file_dir = os.path.join(back_dir, "files", "log_files")
    print(train_file_dir)
    print(log_file_dir)

    model_dir = os.path.join(back_dir, "models", "trained_model")
    os.makedirs(model_dir, exist_ok=True)
    print(model_dir)

    data = []
    tokenizer = None
    model = None

    #if model is not present, train the model
    if not os.path.exists(model_dir):
        model_name = "Salesforce/codet5-small"
        cache_dir = os.path.join(back_dir, "cache_directory")
        tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name, cache_dir=cache_dir)

        # Load dataset
        json_dir = os.path.join(train_file_dir, "train.json")
        with open(json_dir, "r") as f:
            data = json.load(f)

    else:
        # Load the model and tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_dir)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)

        # Load dataset
        json_dir = os.path.join(log_file_dir, "train.json")
        with open(json_dir, "r") as f:
            data = json.load(f)

            if not data:
                raise Exception("No data found in the training file")
            elif not isinstance(data, list):
                raise Exception("Data should be a list of dictionaries")
            elif len(data) < 50:
                raise Exception("Data should contain at least 50 entries")
            
    
    # Preprocess dataset
    preprocessed_data= preprocess_data(train_file_dir, data)

    train_data, eval_data = train_test_split(preprocessed_data, test_size=0.2, random_state=42) # Split the data into training and evaluation sets

    train_dataset = Dataset.from_list(train_data).map(preprocess_function, batched=True)
    eval_dataset = Dataset.from_list(eval_data).map(preprocess_function, batched=True) 

    output_dir = os.path.join(back_dir, "models", "trained_model")
    logging_dir = os.path.join(back_dir, "model_logs")

    # Fine-tuning arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        save_strategy="epoch",
        eval_strategy="epoch",
        learning_rate=5e-5,
        num_train_epochs=10,
        per_device_train_batch_size=4,
        weight_decay=0.01,
        save_total_limit=2,
        logging_dir=logging_dir,
        logging_steps=10,
        push_to_hub=False,
        load_best_model_at_end=True, # Add this line to enable loading the best model
        metric_for_best_model="eval_loss", # Add this line to specify the metric to use
        report_to="none",
    )

    # Trainer
    trainer = Trainer(
        model=model,
        tokenizer=tokenizer,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator= DataCollatorForSeq2Seq(tokenizer, model),
        callbacks=[EarlyStoppingCallback(early_stopping_patience=3)],
    )

    # Train the model
    trainer.train()

    # Save the model and tokenizer
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)

    print("Model trained successfully")