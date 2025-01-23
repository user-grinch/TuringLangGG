import re
from enum import Enum

class eVarType(Enum):
    Boolean = 1
    Int = 2
    Real = 3
    String = 4
    
class Var:
    def __init__(self, var_type: eVarType, val: str):
        self.type = var_type
        self.val = val

    def __str__(self):
        return f"Var(type={self.type}, val={self.val})"

    def __repr__(self):
        return self.__str__()

class VarStore:
    __store: dict[str, Var] = {}

    @staticmethod
    def __getVarType(name: str) -> eVarType:
        name = name.lower()
        if name == "int":
            return eVarType.Int
        elif name == "real":
            return eVarType.Real
        elif name == "boolean":
            return eVarType.Boolean
        else:
            return eVarType.String

    @staticmethod
    def __getDefaultValue(var_type: eVarType) -> str:
        if var_type == eVarType.Int:
            return "0"
        elif var_type == eVarType.Real:
            return "0.0"
        elif var_type == eVarType.Boolean:
            return "false"  
        else:
            return ""
        
    @classmethod
    def getVariables(cls) -> dict[str, Var]:
        return cls.__store

    @classmethod
    def add(cls, expression: str) -> bool:
        # Expression format: var name :type = value
        pattern = r"var\s+(\w+)\s*:\s*(\w+)\s*(?:=\s*(\S+))?"
        match = re.match(pattern, expression)
        
        if match is None:
            return False

        name, type_str, val = match.groups()
        var_type = cls.__getVarType(type_str)

        if val is None:
            val = cls.__getDefaultValue(var_type)
        
        cls.__store[name] = Var(var_type, val)
        return True

    @classmethod
    def get(cls, name: str) -> Var:
        if name not in cls.__store:
            raise KeyError(f"Variable '{name}' not found in store.")
        return cls.__store[name]
