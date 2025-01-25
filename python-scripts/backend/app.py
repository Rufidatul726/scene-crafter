from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from utils.constants import get_template

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

# Define a function to generate code
@app.post("/generate_scene/")
async def generate_scene(request: Request):
    try:
        # Get the input text from the request
        data = await request.json()
        print(data)
        prompt = data.get("prompt")
        if not prompt:
            raise HTTPException(status_code=400, detail="Input text missing")
        # Load the model and tokenizer
        model_name = "./models/trained_model"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        template= get_template("tscn")
        prompt = template + prompt
        
        # Tokenize and generate .tscn content
        inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
        outputs = model.generate(inputs.input_ids, max_length=512)
        tscn_content = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Save the .tscn file
        filename = f"generated_scene_{hash(prompt)}.tscn"
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of app.py
        one_level_back = os.path.normpath(base_dir + os.sep + os.pardir)
        two_levels_back = os.path.normpath(one_level_back + os.sep + os.pardir)
        print(two_levels_back)
        output_dir = os.path.join(two_levels_back, "godot-scene-generation","scene-crafter-generated-scene")
        # output_dir = os.path.join("..", "scene_gen", "scene_crafter_gen_scene")
        os.makedirs(output_dir, exist_ok=True)
        print(output_dir)
        file_path = os.path.join(output_dir, filename)
        with open(file_path, "w") as f:
            f.write(tscn_content)

        return {"message": "Scene generated successfully", "file": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run the app with uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)


