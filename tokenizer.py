

class Tokenizer():
    __instructions : dict[int, list[str]] = {}
    __curLine: int = 1

    @classmethod
    def __trimComments(cls, cmd: str) -> str:
        return cmd.split('%', 1)[0].strip()
    
    @classmethod
    def getInstructions(cls) -> dict[int, list[str]]:
        return cls.__instructions

    @classmethod
    def process(cls, line: str):
        line = Tokenizer.__trimComments(line)

        if len(line) == 0:
            return
        
        cmds: list[str] = line.split(' ', 1)
        
        if len(cmds) > 0:
            cls.__instructions[cls.__curLine] = cmds
            cls.__curLine += 1