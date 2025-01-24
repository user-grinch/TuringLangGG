from instructions.interface.ibase import IBaseInstruction
from parser.expression import ExpressionHandler
from varstore import Var, VarStore


class CMD_Put(IBaseInstruction):
    """
    CMD_Put Class:
    Implements the `put` command, mimicking Turing's `put` statement.
    - This command supports displaying strings and variables.
    - It allows combining strings and variables, suppressing newlines with `..`.

    Example Usage:
        put "Hello, ", name ..
        Output: If `name` contains "World", the result is:
        Hello, World

    Methods:
    --------
    1. getPrefix() -> str:
        Returns the command prefix associated with this class (e.g., 'put').

    2. execute(prefix: str, other: str) -> bool:
        Processes the output (strings and variables) and displays it.
    """
    def getPrefix() -> str:
        return 'put'

    def execute(prefix: str, other: str) -> bool:
        skipNewline = other.endswith('..')

        if skipNewline:
            other = other[0:-2].strip()
        
        lst = other.split(',')

        for str in lst:
            line = str.strip()
            if line.startswith(('"', "'")) and line.endswith(('"', "'")):
                print(line[1:-1], end="")
            else:
                if VarStore.doesExist(line):
                    data: Var = VarStore.get(line)
                    print(data.val, end="")
                # else:
                #     print("Formatting Error: Missing ' or \"")
        if not skipNewline:
            print()
        return True


class CMD_Get(IBaseInstruction):
    """
    CMD_Get Class:
    Implements the `get` command, allowing user input to be stored in variables.
    - This command reads input from the user and assigns it to a variable within VarStore.
    - It ensures the variable name is valid before storing the input.

    Example Usage:
        get myVar
        User Input: Hello World
        Result: The variable 'myVar' in VarStore will hold 'Hello World'.

    Methods:
    --------
    1. getPrefix() -> str:
        Returns the command prefix associated with this class (e.g., 'get').

    2. execute(prefix: str, name: str) -> bool:
        Checks if the variable name is valid, prompts the user for input, and stores the input.
    """
    def getPrefix() -> str:
        return 'get'

    def execute(prefix: str, name: str) -> bool:
        if VarStore.doesExist(name):
            data = input()
            curVar :Var = VarStore.get(name)
            return VarStore.add(name, Var(curVar.type, data))
        else:
            print("Unknown identifier ", name)
            return False