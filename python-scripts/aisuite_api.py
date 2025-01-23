import aisuite as ai
from dotenv import load_dotenv
import os

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
client = ai.Client()

# model= ["huggingface:minosu/godot_dodo_4x_60k_llama_7b"]
provider_name = "huggingface"
model_name = "meta-llama/Llama-3.2-3B-Instruct"
model = f"{provider_name}:{model_name}"

message = "I want to create a script in Godot Engine that creates a new scene with a player character and a camera."

response = client.chat.completions.create(
        model=model,
        messages=[message],
        max_tokens=150,
        temperature=0.75,
        device="cpu",
    )