tokenizer= None

def get_tokenizer():
    global tokenizer
    if tokenizer is None:
        raise ValueError("Tokenizer has not been set. Please set the tokenizer before using it.")
    return tokenizer

def set_tokenizer(tokenizer_name):
    global tokenizer
    tokenizer = tokenizer_name