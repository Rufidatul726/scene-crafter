import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response, status
from groq import Groq

app = FastAPI()
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

SYSTEM_TEMPLATE = """The code should be in GDScript in Godot Engine. 
A project is already created in the engine. Just do as the user asks. Do not write extra explanations.
Always strictly adhere to the format.

Task:
Create a scene with a moving camera, a player character with basic physics, and background music. Generate a `.tscn` file directly, with no additional comments or steps.
If you're creating a file remember the file folder structure: res://scene-crafter-generated-scene. then the file name should be there. do not forget to include the file extension. 
If the user is asking for generating a scene, you should generate a .tscn file and no need to say the steps or explaination. like this:
```
[gd_scene load_steps=2 format=2]
[sub_resource type="PackedScene" id=1]
resource_name = "Main"
class_name = "Node"
```
If the user is asking for generating a script, you should create a .gd file and and no need to say the steps or explaination.like this:
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

@app.post("/recommend/")
async def generate_recommendation(messages: Request):
    messages = await messages.json()
    message = messages.get("message")
    messages = [{"role": "user", "content": message}]
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
    )

    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""
    return {"response": response}

@app.post("/generate")
async def generate_response(request: Request):
    try:
        input_data = await request.json()
        user_input = input_data.get("input")
        if not user_input:
            return Response(content="Input text missing", status_code=status.HTTP_400_BAD_REQUEST)
        
        user_input = SYSTEM_TEMPLATE + user_input

        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "system", "content": user_input}],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
        )

        response = ""
        for chunk in completion:
            print(chunk.choices[0].delta.content)
            response += chunk.choices[0].delta.content or ""
        return {"response": response}
    except Exception as e:
        print(e)
        return {"response": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)