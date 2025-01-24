from exceptions.exceptions import TypeConversionException, UnknownIdentifierException
from parser.expression import ExpressionHandler
from parser.instruction import InstructionHandler
from tokenizer import Tokenizer


class TokenParser():
    '''
        Parses tokens and executes expressions & instructions
    '''
    def __isExpression(list :list[str]):
        return any('var' in string or ':=' in string for string in list)
    
    @classmethod
    def process(cls):
        tokens = Tokenizer.getInstructions()
        
        for k, v in tokens.items():
            try:
                if cls.__isExpression(v):
                    ExpressionHandler.parse(v[0], v[1])
                else:
                    InstructionHandler.parse(v[0], v[1])
            except UnknownIdentifierException as e:
                print(f"Line {k}: Unknown identifier '{e.name}'")
                break
            except TypeConversionException as e:
                print(f"Line {k}: Type conversion from '{e.current}' to {e.required} failed")
                break