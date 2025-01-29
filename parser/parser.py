from exceptions.exception import TypeConversionException, UnknownIdentifierException, UnknownInstructionException
from parser.conditional import ConditionalHandler
from parser.expression import ExpressionHandler
from parser.instruction import InstructionHandler
from parser.loops import LoopHandler
from tokenizer import Tokenizer


class TokenParser():
    '''
        Parses tokens and executes expressions & instructions
    '''
    def __is_expression(lst: list[str]) -> bool:
        return any(
            "var" in string or ":=" in string
            for string in lst
        )

    def __is_conditional(lst: list[str]) -> bool:
        return any("if" in string for string in lst) or \
            any("elsif" in string for string in lst) or \
            any("else" in string for string in lst)

    def __is_loop(lst: list[str]) -> bool:
        return any("loop" in string for string in lst) or \
            any("repeat" in string for string in lst) or \
            any("end loop" in string for string in lst) or \
            any("until" in string for string in lst) or \
            any("exit when" in string for string in lst) or \
            any("while" in string for string in lst) or \
            any("end while" in string for string in lst) 

    @classmethod
    def process(cls):
        tokens = Tokenizer.getInstructions()
        
        idx: int = 0
        keys = list(tokens.keys())
        while idx < len(keys):
            line: int = keys[idx]
            token: list[str] = tokens[keys[idx]]

            route: int = LoopHandler.parseAndRoute(" ".join(token), idx)
            if cls.__is_loop(token) and not LoopHandler.is_exiting():
                if route > 0:
                    idx = route
            else:
                
                validIteration: bool = True
                if LoopHandler.is_in_loop() and LoopHandler.is_exiting():
                    validIteration = False

                if validIteration:
                    if cls.__is_expression(token):
                        ExpressionHandler.parse(token[0], token[1])
                    elif cls.__is_conditional(token):
                        ConditionalHandler.parse("".join(token))
                    else:
                        prefix: str = token[0]
                        args: str = ''

                        if (len(token) > 1):
                            args = token[1]

                        if ConditionalHandler.is_in_condition():
                            if ConditionalHandler.is_condition_active():
                                InstructionHandler.parse(prefix, args)
                        else:
                            InstructionHandler.parse(prefix, args)
            try:
                pass
            except UnknownIdentifierException as e:
                print(f"Line {line}: Unknown identifier '{e.name}'")
                break
            except TypeConversionException as e:
                print(f"Line {line}: Type conversion from '{e.current}' to {e.required} failed")
                break
            except UnknownInstructionException as e:
                print(f"Line {line}: Unknown instruction '{e.name}'")
                break
            except Exception as e:
                print(f"Unknown error occured {e.args}")
                break

            idx += 1