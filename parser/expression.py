import re
from exceptions.exceptions import TypeConversionException
from util import Util
from varstore import Var, VarStore, eVarType


class ExpressionHandler():

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
    def __getDefaultValue(var_type: eVarType):
        if var_type == eVarType.Int:
            return 0
        elif var_type == eVarType.Real:
            return 0.0
        elif var_type == eVarType.Boolean:
            return False
        else:
            return ""
        
    @staticmethod
    def convertToType(val: str, var_type: eVarType):
        try:
            if var_type == eVarType.Int:
                return int(val)
            elif var_type == eVarType.Real:
                return float(val)
            elif var_type == eVarType.Boolean:
                return val in ("true", "1")
            else:
                return ""
        except:
            raise TypeConversionException(var_type, eVarType.String)
            
        
    @classmethod
    def __parseVarInit(cls, expression: str) -> bool:
        # Expression format: var name :type = value
        pattern = r"var\s+(\w+)\s*:\s*(\w+)\s*(?::=\s*(\S+))?"
        match = re.match(pattern, expression)
        
        if match is None:
            return False

        name, type_str, val = match.groups()
        var_type = cls.__getVarType(type_str)

        if val is None:
            val = cls.__getDefaultValue(var_type)

        val = cls.convertToType(val, var_type)
        
        if var_type == eVarType.String:
            if Util.is_quoted(val):
                val = val[1:-1]
        
        return VarStore.add(name, Var(var_type, val))

    @classmethod
    def __parseVarUpdate(cls, name: str, args: str) -> bool:
        args = args.strip(':=').strip() # remove thr assignment operator
        val = eval(args, VarStore.getTable())
        VarStore.update(name, val)

    @classmethod
    def parse(cls, prefix: str, args: str) -> bool:
        if prefix == 'var':
            cls.__parseVarInit(prefix + ' ' +  args)
        else:
            cls.__parseVarUpdate(prefix, args)