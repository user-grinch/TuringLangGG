from varstore import VarStore

class LoopHandler:
    _loop_stack = []

    @classmethod
    def is_in_loop(cls) -> bool:
        return bool(cls._loop_stack)

    @classmethod
    def is_exiting(cls) -> bool:
        return cls.is_in_loop() and cls._loop_stack[-1]["should_exit"]

    @classmethod
    def parse_and_route(cls, expression: str, line: int) -> int:
        expression = expression.strip()

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

        return -1

    @classmethod
    def exit_current(cls):
        if cls.is_in_loop():
            cls._loop_stack[-1]["should_exit"] = True

    @classmethod
    def _start_loop(cls, line: int) -> int:
        cls._loop_stack.append({"start_line": line, "should_exit": False, "condition": None})
        return -1

    @classmethod
    def _start_while(cls, expression: str, line: int) -> int:
        parts = expression.split(' ', 1)
        if len(parts) < 2:
            raise SyntaxError("Invalid while statement: missing condition")

        condition = parts[1].strip()

        if cls.is_in_loop() and cls._loop_stack[-1]["should_exit"]:
            cls._loop_stack.append({"start_line": line, "should_exit": True, "condition": condition})
            return -1

        if not eval(condition, VarStore.getTable()):
            cls._loop_stack.append({"start_line": line, "should_exit": True, "condition": condition})
            return -1
        
        cls._loop_stack.append({"start_line": line, "should_exit": False, "condition": condition})
        return -1

    @classmethod
    def _handle_until(cls, expression: str) -> int:
        _, condition = expression.split(' ', 1)
        if eval(condition, VarStore.getTable()):
            cls.exit_current()

        return cls._end_loop()

    @classmethod
    def _start_for(cls, expression: str, line: int) -> int:
        parts = expression.split(' ', 1)
        if len(parts) < 2:
            raise SyntaxError("Invalid for statement: missing range expression")

        range_expr = parts[1].strip()
        step = 1

        if " by " in range_expr:
            range_expr, step_str = range_expr.split(" by ")
            step = int(step_str.strip())
        
        if ".." not in range_expr:
            raise SyntaxError("Invalid for statement: missing '..' in range expression")

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
        return -1

    @classmethod
    def _end_loop(cls) -> int:
        if not cls.is_in_loop():
            return -1  

        loop = cls._loop_stack[-1]

        if loop["should_exit"]:
            cls._loop_stack.pop()
            return -1  

        if "var" in loop: 
            val = loop["cur"]

            if val + loop["step"] < loop["end"]:
                val += loop["step"]
                cls._loop_stack[-1]["cur"] = val
                VarStore.update(loop["var"], val)
            else:
                cls._loop_stack.pop()
                return -1

        if "condition" in loop:
            if not eval(loop["condition"], VarStore.getTable()):
                cls._loop_stack.pop()
                return -1
            else:
                return loop["start_line"]
        return loop["start_line"]
