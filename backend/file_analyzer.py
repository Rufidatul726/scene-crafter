from transformers import pipeline
import torch
import sys

torch.manual_seed(0)
# generator = pipeline('text-generation', model = 'openai-community/gpt2')

def main():
    # Get the body text from command-line arguments
    body_text = sys.argv[1]  # This gets the text passed from the GDScript
    
    # Process the body text (for example, print it)
    print(f"Received body text: {body_text}")

# Call the main function to execute the script
if __name__ == "__main__":
    main()