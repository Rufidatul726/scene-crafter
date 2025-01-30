from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from utils.constants import get_template
from utils.finetune import train
from utils.postprocess.index import validate
from utils.monitoring.log import add_entry_in_logger
from utils.getscript import process_prompt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the scene generation API!"}

@app.get("getdir")
def get_dir():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(base_dir, "files", "log_files")
    os.makedirs(log_dir, exist_ok=True)
    return {"message": log_dir}

# Define an endpoint to train the model
@app.get("/train_model/")
async def train_model():
    try:
        await train()
        return {"message": "Model trained successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Define a function to generate code
@app.post("/generate_scene/")
async def generate_scene(request: Request):
    try:
        # Get the input text from the request
        data = await request.json()
        print(data)
        prompt = data.get("prompt")
        path= data.get("path")
        if not prompt:
            raise HTTPException(status_code=400, detail="Input text missing")
        # Load the model and tokenizer
        model_name = "./models/trained_model"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        
        # Tokenize and generate .tscn content
        inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
        outputs = model.generate(inputs.input_ids, max_length=512)
        tscn_content = tokenizer.decode(outputs[0], skip_special_tokens=True)

        tscn_content=validate(scene_content=tscn_content, path=path, prompt=prompt)
        # script_content= process_prompt(prompt= scene_content)
        

        # Save the .tscn file
        filename = f"generated_scene_{hash(prompt)}.tscn"
        
        output_dir = os.path.join(path, "scene-crafter-generated-scene")
        os.makedirs(output_dir, exist_ok=True)
        print(output_dir)
        file_path = os.path.join(output_dir, filename)
        with open(file_path, "w") as f:
            f.write(tscn_content)

        add_entry_in_logger(prompt, file_path)
        return {"message": "Scene generated successfully", "file": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run the app with uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)


