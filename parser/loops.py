from util import Util
from varstore import VarStore

class LoopHandler:
    _loop_stack = []
    _route = 0

    @classmethod
    def is_in_loop(cls) -> bool:
        return len(cls._loop_stack) > 0

    @classmethod
    def is_exiting(cls) -> bool:
        return cls.is_in_loop() and cls._loop_stack[-1]["should_exit"]
    
    @classmethod
    def get_route(cls) -> int:
        return cls._route

    @classmethod
    def try_parse(cls, token: str, line: int) -> int:
        expression = " ".join(token).strip()

        if expression.startswith(("loop", "repeat")):
            return cls._start_loop(line)
        elif expression.startswith("while"):
            return cls._start_while(expression, line)
        elif expression.startswith(("end loop", "end while", "end for")):
            return cls._end_loop()
        elif expression.startswith("until"):
            return cls._handle_until(expression)
        elif expression.startswith("for"):
            return cls._start_for(expression, line)

        return False

    @classmethod
    def exit_current(cls):
        if cls.is_in_loop():
            cls._loop_stack[-1]["should_exit"] = True

    @classmethod
    def _start_loop(cls, line: int) -> bool:
        cls._loop_stack.append({"start_line": line, "should_exit": False, "condition": None})
        cls._route = 0
        return True

    @classmethod
    def _start_while(cls, expression: str, line: int) -> bool:
        parts = expression.split(' ', 1)
        if len(parts) < 2:
            raise Exception("Invalid while statement: missing condition")

        condition = parts[1].strip()

        if cls.is_in_loop() and cls._loop_stack[-1]["should_exit"]:
            cls._loop_stack.append({"start_line": line, "should_exit": True, "condition": condition})
            cls._route = 0
            return True

        if not Util.evaluate_condition(condition):
            cls._loop_stack.append({"start_line": line, "should_exit": True, "condition": condition})
            cls._route = 0
            return True
        
        cls._loop_stack.append({"start_line": line, "should_exit": False, "condition": condition})
        cls._route = 0
        return True

    @classmethod
    def _handle_until(cls, expression: str) -> bool:
        _, condition = expression.split(' ', 1)

        if Util.evaluate_condition(condition):
            cls.exit_current()

        cls._end_loop()
        return True

    @classmethod
    def _start_for(cls, expression: str, line: int) -> bool:
        parts = expression.split(' ', 1)
        if len(parts) < 2:
            raise Exception("Invalid for statement: missing range expression")

        range_expr = parts[1].strip()
        step = 1

        if " by " in range_expr:
            range_expr, step_str = range_expr.split(" by ")
            step = int(step_str.strip())
        
        if ".." not in range_expr:
            raise Exception("Invalid for statement: missing '..' in range expression")

        var, range_str = range_expr.split(":")
        var = var.strip()
        start, end = range_str.split("..")
        start = int(start.strip())
        end = int(end.strip()) + 1  

        cls._loop_stack.append({
            "start_line": line,
            "should_exit": False,
            "start": start,
            "cur": start,
            "end": end,
            "step": step,
            "var": var
        })
        cls._route = 0
        return True

    @classmethod
    def _end_loop(cls) -> bool:
        if not cls.is_in_loop():
            cls._route = 0  
            return True

        loop = cls._loop_stack[-1]

        if loop["should_exit"]:
            cls._loop_stack.pop()
            cls._route = 0  
            return True

        if "var" in loop: 
            val = loop["cur"]

            if val + loop["step"] < loop["end"]:
                val += loop["step"]
                cls._loop_stack[-1]["cur"] = val
                VarStore.update(loop["var"], val)
            else:
                cls._loop_stack.pop()
                cls._route = 0
                return True

        if "condition" in loop and loop["condition"]:
            if not Util.evaluate_condition(loop["condition"]):
                cls._loop_stack.pop()
                cls._route = 0
                return True
        cls._route = loop["start_line"]
        return True
