from exceptions.exceptions import UnknownInstructionException
from instructions.io import CMD_Get, CMD_Put
from instructions.interface.ibase import IBaseInstruction

class InstructionHandler():
    __commands: list[IBaseInstruction] = [
        CMD_Put, CMD_Get
    ]

    @classmethod
    def findHandler(cls, prefix: str) -> IBaseInstruction:
        for e in cls.__commands:
            if e.getPrefix() == prefix:
                return e
            
        raise UnknownInstructionException(prefix)
    
    @classmethod
    def parse(cls, prefix: str, args: str) -> bool:
        handler: IBaseInstruction = cls.findHandler(prefix)
        return handler.execute(prefix, args)