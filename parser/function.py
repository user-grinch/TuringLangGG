import re
from varstore import Var, VarStore, eVarType

class FunctionDef:
    name: str
    rtnType: eVarType
    params: list[str]
    start: int
    end: int

    def __init__(self, name: str, params: list[str], rtnType: eVarType, start: int):
        self.name = name
        self.rtnType = rtnType
        self.params = params
        self.start = start

class FunctionHandler(): 
    _definations: list[FunctionDef] = []
    _route = 0
    _isInFunction = False

    @classmethod
    def try_parse(cls, token: list[str], line) -> bool:
        if token[0].startswith("function") or token[0].startswith("procedure"):
            return cls.__handle_start(token[1], line)
        elif len(cls._definations) > 0 \
        and token[0].startswith("end") \
        and token[1].startswith(cls._definations[-1].name):
            return cls.__handle_end(token[1], line)
        else: 
            return cls._isInFunction

    @classmethod
    def get_route(cls) -> int:
        return cls._route
    
    @classmethod
    def __handle_start(cls, token: str, line: int):
        match = re.match(r'(\w+)\s*\(\s*([^)]*)\s*\)\s*:?\s*(\w+)?', token)

        if not match:
            raise Exception(f"Not a function statement {match}")
        
        name: str = match.group(1)
        params: str = match.group(2) if match.group(2) else None
        rtn: eVarType = Var.get_var_type(match.group(3)) if match.group(3) else None

        fdef: FunctionDef = FunctionDef(name, params, rtn, line)
        cls._definations.append(fdef)    
        cls._isInFunction = True
        
        return True
    
    @classmethod
    def __handle_end(cls, token: str, line):
        cls._definations[-1].end = line;
        cls._isInFunction = False

        return True