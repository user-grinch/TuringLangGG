
from instructions.interface.icommnad import ICommand


class CMD_Unknown(ICommand):
    def getPrefix() -> str:
        return 'unknown'

    def execute(prefix: str, other: str) -> bool:
        print(f"Unknown '{prefix}' with arguments [{other}]")
        return True;