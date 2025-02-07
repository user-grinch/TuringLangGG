import re
from exceptions.exception import TypeConversionException
from util import Util
from varstore import Var, VarStore, eVarType


class ExpressionHandler():
    @classmethod
    def try_parse(cls, token: list[str]) -> bool:
        if cls.__is_valid(token):
            prefix: str = token[0]
            args: str = token[1]
            if prefix == 'var':
                cls.__parse_var_init(prefix + ' ' +  args)
            else:
                cls.__parse_var_update(prefix, args)
            return True
        return False
        
    @classmethod
    def __parse_var_init(cls, expression: str) -> bool:
        # Expression format: var name :type = value
        pattern = r"var\s+(\w+)\s*:\s*(\w+)\s*(?::=\s*(.+))?"
        match = re.match(pattern, expression.strip())
        
        if match is None:
            return False

        name, type_str, val = match.groups()
        var_type = Var.get_var_type(type_str)

        if val is None:
            val = Var.get_default_value(var_type)

        val = Var.convert_to_type(val, var_type)
        
        if var_type == eVarType.String:
            if Util.is_quoted(val):
                val = val[1:-1]
        
        return VarStore.add(name, Var(var_type, val))

    @classmethod
    def __parse_var_update(cls, name: str, args: str) -> bool:
        args = args.strip(':=').strip() # remove thr assignment operator
        val = Util.evaluate_condition(args)    
        VarStore.update(name, val)

    @staticmethod
    def __is_valid(lst: list[str]) -> bool:
        '''
            Return true if the list passed is a expression statement
        '''
        return any(
            "var" in string or ":=" in string
            for string in lst
        )