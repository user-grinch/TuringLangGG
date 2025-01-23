from instructions.handler import InstructionHandler
from tokenizer import Tokenizer


class Parser():
    def process():
        tokens = Tokenizer.getInstructions()
        
        for k, v in tokens.items():
            InstructionHandler.execute(v[0], v[1])