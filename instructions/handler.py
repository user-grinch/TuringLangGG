from instructions.io import CMD_Get, CMD_Put
from instructions.unknown import CMD_Unknown
from instructions.interface.ibase import IBaseInstruction
from instructions.var import CMD_Var

class InstructionHandler():
    __commands: list[IBaseInstruction] = [
        CMD_Put, CMD_Unknown, CMD_Var, CMD_Get
    ]

    def register(cmd: IBaseInstruction):
        InstructionHandler.__commands.append(cmd)

    def findHandler(prefix: str) -> IBaseInstruction:
        for e in InstructionHandler.__commands:
            if e.getPrefix() == prefix:
                return e
            
        return CMD_Unknown
    
    def execute(prefix: str, args: str) -> bool:
        handler: IBaseInstruction = InstructionHandler.findHandler(prefix)
        return handler.execute(prefix, args)

    