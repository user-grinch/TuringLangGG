
from instructions.interface.ibase import IBaseInstruction
from varstore import VarStore

class CMD_Var(IBaseInstruction):
    def getPrefix() -> str:
        return 'var'

    def execute(prefix: str, other: str) -> bool:
        return VarStore.parse(prefix + ' ' + other)