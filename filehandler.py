from tokenizer import Tokenizer

class FileHandler():
    def process(filePath: str):
        with open(filePath, 'r') as file:
            for line in file:
                text :str = line.strip()
                if len(text) > 0:
                    Tokenizer.process(text);