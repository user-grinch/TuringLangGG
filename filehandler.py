from tokenizer import Tokenizer

class FileHandler():
    def process(filePath: str):
        with open(filePath, 'r') as file:
            for line in file:
                Tokenizer.process(line);