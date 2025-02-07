from exceptions.exception import TypeConversionException, UnknownIdentifierException, UnknownInstructionException
from parser.conditional import ConditionalHandler
from parser.expression import ExpressionHandler
from parser.function import FunctionHandler
from parser.instruction import InstructionHandler
from parser.loops import LoopHandler
from tokenizer import Tokenizer


class TokenParser():
    '''
        Parses tokens and executes expressions & instructions
    '''
    @classmethod
    def process(cls):
        tokens = Tokenizer.getInstructions()

        idx: int = 0
        keys = list(tokens.keys())
        while idx < len(keys):
            line: int = keys[idx]
            token: list[str] = tokens[keys[idx]]

            try:
                idx = cls.__process_token(token, idx)
            except Exception as e:
                cls.__handle_error(line, e)

            idx = idx + 1

    @staticmethod
    def __process_token(token: list[str], idx: int):
        if FunctionHandler.try_parse(token, idx):
            route = FunctionHandler.get_route()
            if route > 0:
                idx = route
        elif LoopHandler.try_parse(token, idx):
            route = LoopHandler.get_route()
            if route > 0:
                idx = route
        else:
            iterValid: bool = not LoopHandler.is_exiting()
            if iterValid:
                if ExpressionHandler.try_parse(token):
                    pass
                elif ConditionalHandler.try_parse(token):
                    pass
                elif not ConditionalHandler.is_in_condition() or ConditionalHandler.is_condition_active():
                    InstructionHandler.try_parse(token)

        return idx

    @staticmethod
    def __handle_error(line: int, error: Exception):
        if isinstance(error, UnknownIdentifierException):
            print(f"Line {line}: Unknown identifier '{error.name}'")
        elif isinstance(error, TypeConversionException):
            print(f"Line {line}: Type conversion from '{error.current}' to {error.required} failed")
        elif isinstance(error, UnknownInstructionException):
            print(f"Line {line}: Unknown instruction '{error.name}'")
        else:
            print(f"Line {line}: {error}")
