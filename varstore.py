from enum import Enum

from exceptions.exception import UnknownIdentifierException

class eVarType(Enum):
    Boolean = 1
    Int = 2
    Real = 3
    String = 4
    
class Var:
    def __init__(self, var_type: eVarType, val):
        self.type = var_type
        self.val = val

    def __str__(self):
        return f"Var(type={self.type}, val={self.val})"

    def __repr__(self):
        return self.__str__()

class VarStore:
    __store: dict[str, Var] = {}
        
    # Returns the internal Var structure dict
    @classmethod
    def getVarTable(cls) -> dict[str, Var]:
        return cls.__store

    # Returns a formatted key value pair dict
    @classmethod
    def getTable(cls) -> dict[str, object]:
        table = {}
        for key, var in cls.__store.items():
            table[key] = var.val
        return table
    
    @classmethod
    def add(cls, name: str, data: Var) -> bool:
        from parser.expression import ExpressionHandler

        data.val = ExpressionHandler.convert_to_type(data.val, data.type)

        cls.__store[name] = Var(data.type, data.val)
    
    @classmethod
    def update(cls, name: str, val: object) -> bool:
        if cls.doesExist(name):
            data :Var = cls.get(name)
            data.val = val
            cls.add(name, data)
        else:
            raise UnknownIdentifierException(name)

    @classmethod
    def doesExist(cls, name: str) -> bool:
        return name in cls.__store

    @classmethod
    def get(cls, name: str) -> Var:
        if name not in cls.__store:
            raise KeyError(f"Variable '{name}' not found in store.")
        return cls.__store[name]
