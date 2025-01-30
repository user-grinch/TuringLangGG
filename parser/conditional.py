import re
from util import Util
from varstore import VarStore

class ConditionalHandler:
    __conditionalStack = []

    @classmethod
    def is_in_condition(cls) -> bool:
        return len(cls.__conditionalStack) > 0
    
    @classmethod
    def is_condition_active(cls) -> bool:
        if not cls.__conditionalStack:
            return False
        return cls.__conditionalStack[-1]["lastConditionResult"]

    @classmethod
    def try_parse(cls, lst: list[str]) -> bool:
        expression: str = " ".join(lst)
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
    def _handle_if(cls, expression: str) -> bool:
        pattern = r"if\s*(.*?)\s*(then|$)"
        match = re.match(pattern, expression)

        if not match:
            raise Exception(f"Not a valid condition {match}")

        condition = match.group(1).strip()
        result = Util.evaluate_condition(condition)
        cls.__conditionalStack.append({
            "lastConditionResult": result,
            "skipRest": result
        })
        return True

    @classmethod
    def _handle_else_if(cls, expression: str) -> bool:
        if not cls.is_in_condition():
            return False

        pattern = r"(else if|elsif)\s*(.*?)\s*(then|$)"
        match = re.match(pattern, expression)

        if not match:
            raise Exception(f"Not a valid condition {match}")

        condition = match.group(2).strip()
        current_scope = cls.__conditionalStack[-1]
        if current_scope["skipRest"]:
            current_scope["lastConditionResult"] = False
        else:
            result = Util.evaluate_condition(condition)
            current_scope["skipRest"] = current_scope["skipRest"] or result
            current_scope["lastConditionResult"] = result

        return True
      

    @classmethod
    def _handle_else(cls) -> bool:
        if not cls.is_in_condition():
            return False

        current_scope = cls.__conditionalStack[-1]
        if current_scope["skipRest"]:
            current_scope["lastConditionResult"] = False
            return False
        
        current_scope["lastConditionResult"] = not current_scope["lastConditionResult"]
        return True

    @classmethod
    def _handle_end_if(cls) -> bool:
        if cls.is_in_condition():
            cls.__conditionalStack.pop()

        return True