import re
from exceptions.exception import UnknownIdentifierException
from instructions.interface.ibase import IBaseInstruction
from parser.expression import ExpressionHandler
from parser.loops import LoopHandler
from util import Util
from varstore import Var, VarStore


class CMD_Exit(IBaseInstruction):
    """
    CMD_Exit Class:
    Implements the `exit` command, mimicking Turing's `exit` statement.
    - It allows exiting loops

    Example Usage:
        exit 
        exit when n > 1

    Methods:
    --------
    1. getPrefix() -> str:
        Returns the command prefix associated with this class

    2. execute(prefix: str, other: str) -> bool:
        Processes the output (strings and variables) and displays it.
    """
    @staticmethod
    def getPrefix() -> str:
        return 'exit'
    
    @classmethod
    def execute(cls, prefix: str, other: str) -> bool:
        shouldExit: bool = True
        
        splits = other.split(' ', 1)
        if (len(splits) >= 2 and splits[0] == 'when'):
            splits[1].replace('=', '==')
            val = eval(splits[1], VarStore.getTable())    
            if val == 0:
                shouldExit = False

        if shouldExit:
            LoopHandler.exit_current()

        return False