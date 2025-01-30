from exceptions.exception import UnknownInstructionException
from instructions.control import CMD_Exit
from instructions.io import CMD_Get, CMD_Put
from instructions.interface.ibase import IBaseInstruction

class InstructionHandler():
    __commands: list[IBaseInstruction] = [
        CMD_Put, CMD_Get, CMD_Exit
    ]
    
    @classmethod
    def try_parse(cls, token: list[str]) -> bool:
        prefix: str = token[0]
        args: str = ''

        if len(token) > 1:
            args = token[1]

        handler: IBaseInstruction = cls.__find_handler(prefix)
        return handler.execute(prefix, args)
    
    @classmethod
    def __find_handler(cls, prefix: str) -> IBaseInstruction:
        for e in cls.__commands:
            if e.getPrefix() == prefix:
                return e
            
        raise UnknownInstructionException(prefix)