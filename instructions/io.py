
from instructions.interface.icommnad import ICommand
from varstore import Var, VarStore

class CMD_Put(ICommand):
    def getPrefix() -> str:
        return 'put'

    def execute(prefix: str, other: str) -> bool:
        lst = other.split(',')

        for str in lst:
            line = str.strip()
            if line.startswith(('"', "'")) and line.endswith(('"', "'")):
                print(line[1:-1], end= "")
            else:
                if VarStore.isValid(line):
                    var :Var =VarStore.get(line)
                    print(var.val, end= "")
                else:
                    print("Formatting Error: Missing ' or \"")
        print();
        return True;