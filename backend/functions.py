import os
import re
from transformers import pipeline

pipe = pipeline("text-generation", model="meta-llama/Llama-3.2-1B")

async def put_text(context_result):
    text_context= f"{context_result}"
    with open("project_context.txt", "a") as f:
        f.write(text_context)

async def generator(context_prompt, max_length=20, num_return_sequences=1):
    try:
        print("generation started....")
        result = pipe(context_prompt, pad_token_id=pipe.tokenizer.eos_token_id, max_new_tokens = max_length)


        print("writing in file...")
        await put_text(result[0]["generated_text"])

        # return result
    except Exception as e:
        print(f"Error during model generation: {e}")
        return {"error": "Model loading or generation failed"}


async def analyze_project(path):
    context = {"scenes": [], "scripts": [], "game": []}
    index = 1 
    for root, _, files in os.walk(path):
        for fileName in files:
            full_path = os.path.join(root, fileName)
            print(f"analyzing...{index}")
            if fileName.endswith(".tscn"):
                with open(full_path, 'r') as f:
                    content = f.read()
                    context["scenes"].append(content)

                    await generator(content)
                # context["scenes"].append(os.path.join(root, file))
            elif fileName.endswith(".gd"):
                with open(full_path, 'r') as f:
                    content = f.read()
                    context["scripts"].append(content)

                    await generator(content)
                # context["scripts"].append(os.path.join(root, file))
            elif fileName == "project.godot":
                with open(full_path, "r") as f:
                    content = f.read()
                    context["game"].append(content)

                    await generator(content)

    # context_prompt = f"{context}"

    # result = await generator(context_prompt, max_length=300, num_return_sequences=1)

    return context
