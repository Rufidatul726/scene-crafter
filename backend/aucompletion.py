from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "microsoft/Phi-3-mini-128k-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)

def autocomplete_code(context, max_tokens=100):
    inputs = tokenizer(context, return_tensors="pt")
    outputs = model.generate(
        inputs["input_ids"],
        max_new_tokens=max_tokens,
        pad_token_id=tokenizer.eos_token_id,
        attention_mask=inputs["attention_mask"]
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


context = " @tool extends EditorPlugin var dock func _enter_tree() -> void: print('Scene Crafter "
suggestion = autocomplete_code(context)
print(suggestion)