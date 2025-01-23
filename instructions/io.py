
from instructions.interface.icommnad import ICommand

class CMD_Put(ICommand):
    def getPrefix() -> str:
        return 'put'

    def execute(prefix: str, other: str) -> bool:
        if other.startswith(('"', "'")) and other.endswith(('"', "'")):
            print(other[1:-1])
        else:
            print("Formatting Error: Missing ' or \"")
        return True;