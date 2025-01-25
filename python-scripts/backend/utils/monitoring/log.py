import os
import json
import datetime

def add_entry_in_logger(prompt, file_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))  
    back_dir = os.path.normpath(base_dir + os.sep + os.pardir)
    back_dir = os.path.normpath(back_dir + os.sep + os.pardir)
    print(back_dir)
    log_file_dir = os.path.join(back_dir, "files", "log_files")
    train_file= os.path.join(log_file_dir, "train.json")

    if not os.path.exists(log_file_dir):
        raise Exception("Log file directory does not exist")
    if not os.path.exists(train_file):
        raise Exception("Train file does not exist")
    
    new_entry = {
        "prompt": prompt,
        "output": file_path,
        "timestamp": datetime.datetime.now().isoformat()
    }

    with open(train_file, "r") as f:
        if os.stat(train_file).st_size == 0:
            data = []
        else:
            data = json.load(f)
        data.append(new_entry)


    with open(train_file, "w") as f:
        json.dump(data, f)

    return {"message": "Entry added to the logger"}