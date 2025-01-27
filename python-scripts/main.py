from fastapi import FastAPI, Request, Response, status
from gpt4all import GPT4All

app = FastAPI()
# model = GPT4All(model_name="Llama-3.2-3B-Instruct-Q4_0.gguf", verbose=True)
model = GPT4All(model_name="qwen2-1_5b-instruct-q4_0.gguf", model_path="E:\Programs\gpt4all")
print("Model loaded successfully.")

SYSTEM_TEMPLATE = """The code should be for Godot Engine. do not give me steps.
If the user is asking for generating a scene, you should create a .tscn file.  like this:
```
[gd_scene load_steps=2 format=2]
[sub_resource type="PackedScene" id=1]
resource_name = "Main"
class_name = "Node"
```
If the user is asking for generating a script, you should create a .gd file. like this:
```
extends Node

func _ready():
    my_var = 5

func _process(delta):
    if Input.is_action_pressed("ui_right"):
    
```
If the user is asking for correcting an error, you should provide the corrected code in that godot {version}.
If the user is asking for a tutorial, you should provide a step-by-step guide.
If the user is asking for a code snippet, you should provide a code snippet.
If the user is asking for a code explanation, you should provide an explanation of the code.
"""

MAX_LENGTH = 8500
MAX_TOKENS = 2048

@app.post("/generate_scene/")
async def generate(request: Request):
    print(request)
    try:
        input_data = await request.json()
        print(input_data)
        user_input = input_data.get("prompt")
        if not user_input:
            return Response(content="Input text missing", status_code=status.HTTP_400_BAD_REQUEST)
        
        user_input = user_input + SYSTEM_TEMPLATE 

        print(user_input)
        response = model.generate(user_input, max_tokens=MAX_LENGTH)
        print(response)
        return {"response": response}
    except Exception as e:
        # Handle errors and return HTTP 500 with the error message
        print(e)
        return Response(content=f"Error: {str(e)}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

