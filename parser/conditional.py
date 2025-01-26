import re

from varstore import VarStore

class ConditionalHandler:
    __inConditional: bool = False
    __lastConditionResult: bool = False
    __skipRest: bool = False

    @classmethod
    def is_in_condition(cls) -> bool:
        return cls.__inConditional
    
    @classmethod
    def is_condition_active(cls) -> bool:
        return cls.__lastConditionResult

    @classmethod
    def parse(cls, expression: str) -> bool:
        expression = expression.strip()

        expression = expression.replace('=', '==')

        if expression.startswith("if"):
            return cls._handle_if(expression)

        elif expression.startswith("elsif"):
            return cls._handle_else_if(expression)

        elif expression.startswith("else"):
            return cls._handle_else()
        elif expression.startswith("end if"):
            return cls._handle_end_if()

        return False 
    
    @classmethod
    def _handle_end_if(cls, expression: str) -> bool:
        cls.reset()
        return True

    @classmethod
    def _handle_if(cls, expression: str) -> bool:
        pattern = r"if\s*(.*?)\s*(then|$)"
        match = re.match(pattern, expression)

        if match is None:
            return False  

        condition = match.group(1).strip()
        try:
            result = cls.evaluate_condition(condition)
            cls.__inConditional = True
            cls.__skipRest = result
            cls.__lastConditionResult = result
            return True
        except Exception as e:
            print(f"Error while evaluating `if` condition: {e}")
            return False

    @classmethod
    def _handle_else_if(cls, expression: str) -> bool:
        if not cls.__inConditional:
            return False

        pattern = r"(else if|elsif)\s*(.*?)\s*(then|$)"
        match = re.match(pattern, expression)

        if match is None:
            return False 

        condition = match.group(2).strip()
        try:
            if cls.__skipRest:
                cls.__lastConditionResult = False
            else:
                result = cls.evaluate_condition(condition)
                cls.__skipRest = cls.__skipRest or result
                cls.__lastConditionResult = result

            return True
        except Exception as e:
            print(f"Error while evaluating `else if` condition: {e}")
            return False

    @classmethod
    def _handle_else(cls) -> bool:
        if not cls.__inConditional or cls.__skipRest:
            cls.__lastConditionResult = False
            return False
        
        cls.__lastConditionResult = not cls.__lastConditionResult
        return True

    @classmethod
    def evaluate_condition(cls, condition: str) -> bool:
        try:
            result = eval(condition, {"__builtins__": None}, VarStore.getTable())
            if not isinstance(result, bool):
                raise ValueError(f"Condition did not evaluate to a boolean: {condition}")
            return result
        except Exception as e:
            raise Exception(f"Failed to evaluate condition '{condition}': {e}")
        
    @classmethod
    def reset(cls):
        cls.__inConditional = False
        cls.__lastConditionResult = False
        cls.__skipRest = False