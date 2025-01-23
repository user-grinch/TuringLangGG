
from instructions.interface.icommnad import ICommand
from varstore import VarStore

class CMD_Var(ICommand):
    def getPrefix() -> str:
        return 'var'

    def execute(prefix: str, other: str) -> bool:
        return VarStore.add(prefix + ' ' + other)