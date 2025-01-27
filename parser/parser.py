from exceptions.exception import TypeConversionException, UnknownIdentifierException, UnknownInstructionException
from parser.conditional import ConditionalHandler
from parser.expression import ExpressionHandler
from parser.instruction import InstructionHandler
from tokenizer import Tokenizer


class TokenParser():
    '''
        Parses tokens and executes expressions & instructions
    '''
    def __is_expression(list :list[str]):
        return any('var' in string or ':=' in string for string in list)
    
    def __is_conditional(list :list[str]):
        return any('if' in string for string in list) or any('elsif' in string for string in list) or any('else' in string for string in list)
    
    @classmethod
    def process(cls):
        tokens = Tokenizer.getInstructions()
        
        for k, v in tokens.items():
            try:
                if cls.__is_expression(v):
                    ExpressionHandler.parse(v[0], v[1])
                elif cls.__is_conditional(v):
                    text = v[0]
                    if (len(v) >= 2):
                        text += v[1]
                    ConditionalHandler.parse(text)
                else:
                    if ConditionalHandler.is_in_condition():
                        if ConditionalHandler.is_condition_active():
                            InstructionHandler.parse(v[0], v[1])
                    else:
                        InstructionHandler.parse(v[0], v[1])

            except UnknownIdentifierException as e:
                print(f"Line {k}: Unknown identifier '{e.name}'")
                break
            except TypeConversionException as e:
                print(f"Line {k}: Type conversion from '{e.current}' to {e.required} failed")
                break
            except UnknownInstructionException as e:
                print(f"Line {k}: Unknown instruction '{e.name}'")
                break
            except Exception as e:
                print(f"Unknown error occured {e.args}")
                break;