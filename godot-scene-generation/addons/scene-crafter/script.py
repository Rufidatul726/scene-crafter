from gpt4all import GPT4All
import json
import sys

async def generate(request):
    try:
        input_data = await request.json()
        user_input = input_data.get("input")
        if not user_input:
            return response(content="Input text missing", status_code=400)
        
        if not hasattr(model, 'generate'):
            return response(content="Model does not have a generate method", status_code=400)
        
        model = GPT4All(model_name="Llama-3.2-3B-Instruct-Q4_0.gguf", model_path="E:\Programs\gpt4all\Llama-3.2-3B-Instruct-Q4_0.gguf")
        response = model.generate(user_input)
        return response({"response": response})
    except Exception as e:
        return response(content=f"Error: {str(e)}", status_code=500)

if __name__ == "__main__":
    # Parse input from command-line arguments
    input_data = json.loads(sys.argv[1])
    user_input = input_data.get("input", "")
    response = generate(user_input)
    print(json.dumps({"response": response}))