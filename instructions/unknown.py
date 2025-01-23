
from instructions.interface.ibase import IBaseInstruction


class CMD_Unknown(IBaseInstruction):
    def getPrefix() -> str:
        return 'unknown'

    def execute(prefix: str, other: str) -> bool:
        print(f"Unknown '{prefix}' with arguments [{other}]")
        return True;