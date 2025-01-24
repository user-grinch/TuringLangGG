from parser.expression import ExpressionHandler
from parser.instruction import InstructionHandler
from tokenizer import Tokenizer


class TokenParser():
    def process():
        tokens = Tokenizer.getInstructions()
        
        for k, v in tokens.items():
            if any(':=' in string for string in v):
                ExpressionHandler.parse(v[0], v[1])
            else:
                InstructionHandler.parse(v[0], v[1])