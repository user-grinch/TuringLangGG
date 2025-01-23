from instructions.io import CMD_Put
from instructions.unknown import CMD_Unknown
from instructions.interface.icommnad import ICommand
from instructions.var import CMD_Var

class InstructionHandler():
    __commands: list[ICommand] = [
        CMD_Put, CMD_Unknown, CMD_Var
    ]

    def register(cmd: ICommand):
        InstructionHandler.__commands.append(cmd)

    def findHandler(prefix: str) -> ICommand:
        for e in InstructionHandler.__commands:
            if e.getPrefix() == prefix:
                return e
            
        return CMD_Unknown
    
    def execute(prefix: str, args: str) -> bool:
        handler: ICommand = InstructionHandler.findHandler(prefix)
        return handler.execute(prefix, args)

    