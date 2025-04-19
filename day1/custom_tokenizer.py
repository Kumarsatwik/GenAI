import re

class CustomTokenizer:
    def __init__(self, special_tokens=None):
        self.token_pattern = re.compile(r'\w+|[^\w\s]')  # Regular expression for tokenization 

    def tokenize(self, text):
        tokens = self.token_pattern.findall(text)
        return tokens

    def detokenize(self, tokens):
        return ' '.join(tokens)

tokenizer = CustomTokenizer()
text = "Hello, world! This is a test!"
tokens = tokenizer.tokenize(text)
print("Tokens:", tokens)
detokenized_text = tokenizer.detokenize(tokens)
print("Detokenized:", detokenized_text)
