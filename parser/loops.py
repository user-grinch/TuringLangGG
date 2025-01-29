from varstore import VarStore


class LoopHandler:
    __loopStack = []
    
    @classmethod
    def is_in_loop(cls) -> bool:
        return len(cls.__loopStack) > 0
    
    @classmethod
    def is_exiting(cls) -> bool:
        if cls.is_in_loop():
            return cls.__loopStack[-1]["shouldExit"]

        return False
    
    @classmethod
    def parseAndRoute(cls, expression: str, line: int) -> int:
        '''
            Returns -1 on exit 
            Else the line number to route to
        '''
        expression = expression.strip()
        if expression.startswith(("loop", "repeat")):
            return cls._handle_loop(line) # Loop body starts from next line

        elif expression.startswith("end loop"):
            return cls._handle_end_loop()
        
        elif expression.startswith("until"):
            return cls._handle_until(expression)

        return -1

    @classmethod
    def exit_current(cls):
        if cls.is_in_loop():
            cls.__loopStack[-1]["shouldExit"] = True

    @classmethod
    def _handle_loop(cls, line: int) -> int:
        cls.__loopStack.append({
            "startLine": line,
            "shouldExit": False 
        })
        return -1
    
    @classmethod
    def _handle_until(cls, expression: str) ->bool:
        splits = expression.split(' ', 1)
        splits[1].replace('=', '==')
        shouldExit = eval(splits[1], VarStore.getTable())  

        if shouldExit:
            cls.__loopStack[-1]["shouldExit"] = True
       
        return cls._handle_end_loop()

    @classmethod
    def _handle_end_loop(cls) -> bool:
        if cls.__loopStack[-1]["shouldExit"]:
            cls.__loopStack[-1]["shouldExit"] = False
            cls.__loopStack.pop()
            return -1
        else:
            return cls.__loopStack[-1]["startLine"]
