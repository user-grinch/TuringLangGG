from varstore import VarStore

class LoopHandler:
    """Handles loop control structures: 'loop', 'repeat', 'while', 'until', and their endings."""
    _loop_stack = []

    @classmethod
    def is_in_loop(cls) -> bool:
        """Checks if currently inside a loop."""
        return bool(cls._loop_stack)

    @classmethod
    def is_exiting(cls) -> bool:
        """Checks if the current loop should exit."""
        return cls.is_in_loop() and cls._loop_stack[-1]["should_exit"]

    @classmethod
    def parse_and_route(cls, expression: str, line: int) -> int:
        """
        Parses loop-related expressions and determines execution flow.
        Returns -1 if execution continues normally, otherwise returns the new line number.
        """
        expression = expression.strip()

        if expression.startswith(("loop", "repeat")):
            return cls._start_loop(line)
        elif expression.startswith("while"):
            return cls._start_while(expression, line)
        elif expression.startswith(("end loop", "end while")):
            return cls._end_loop()
        elif expression.startswith("until"):
            return cls._handle_until(expression)

        return -1

    @classmethod
    def exit_current(cls):
        """Marks the current loop for exit."""
        if cls.is_in_loop():
            cls._loop_stack[-1]["should_exit"] = True

    @classmethod
    def _start_loop(cls, line: int) -> int:
        """Handles 'loop' or 'repeat' statements, which run indefinitely until explicitly exited."""
        cls._loop_stack.append({"start_line": line, "should_exit": False, "condition": None})
        return -1

    @classmethod
    def _start_while(cls, expression: str, line: int) -> int:
        """Handles 'while' statements, storing conditions for evaluation."""
        parts = expression.split(' ', 1)
        if len(parts) < 2:
            raise SyntaxError("Invalid while statement: missing condition")

        condition = parts[1].strip()

        if cls.is_in_loop() and cls._loop_stack[-1]["should_exit"]:
            cls._loop_stack.append({"start_line": line, "should_exit": True, "condition": condition})
            return -1

        # Evaluate the condition at the start of the loop
        if not eval(condition, VarStore.getTable()):  
            cls._loop_stack.append({"start_line": line, "should_exit": True, "condition": condition})
            # If condition is false, skip the loop by returning -1
            return -1
        
        # Condition is True, add loop to stack
        cls._loop_stack.append({"start_line": line, "should_exit": False, "condition": condition})
        return -1  # Continue execution inside loop


    @classmethod
    def _handle_until(cls, expression: str) -> int:
        """Handles 'until <condition>' statements, exiting loops when condition is met."""
        _, condition = expression.split(' ', 1)
        if eval(condition, VarStore.getTable()):  
            cls.exit_current()

        return cls._end_loop()

    @classmethod
    def _end_loop(cls) -> int:
        """Handles 'end loop' or 'end while' statements, controlling loop flow."""
        if not cls.is_in_loop():
            return -1  # Avoid raising an error; just ignore unexpected 'end'

        loop = cls._loop_stack[-1]

        if loop["should_exit"]:  
            cls._loop_stack.pop()
            return -1  # Exit the loop completely

        if loop["condition"]:
            if not eval(loop["condition"], VarStore.getTable()):  
                cls._loop_stack.pop()  # Exit the loop if condition is false
                return -1
            else:
                return loop["start_line"]  # Jump back to loop start
        
        return loop["start_line"]