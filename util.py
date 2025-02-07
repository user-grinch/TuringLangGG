from varstore import VarStore


class Util():
    @staticmethod
    def is_quoted(s: str) -> bool:
        """Check if a string is enclosed in quotes."""
        return s.startswith(('"', "'")) and s.endswith(('"', "'"))
    
    @staticmethod
    def evaluate_condition(condition: str) -> bool:
        if not (condition.find('>=') or condition.find('<=') or condition.find('==')):
            condition = condition.replace('=', '==')
        result = eval(condition, {"__builtins__": None}, VarStore.getTable())
        # if not isinstance(result, bool):
        #     raise ValueError(f"Condition did not evaluate to a boolean: {condition}")
        return result
      