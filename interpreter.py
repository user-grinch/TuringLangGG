import sys
from filehandler import FileHandler
from parser.parser import TokenParser
from varstore import VarStore

class Interpreter():
    @classmethod
    def run(cls):
        if len(sys.argv) > 1:
            FileHandler.process(sys.argv[1]);
            TokenParser.process()
            print(VarStore.getVarTable())
    
    @classmethod
    def debug(cls, string: str):
        FileHandler.process(string);
        TokenParser.process()
        print(VarStore.getVarTable())

if __name__ == '__main__':
    Interpreter.run()
    # Interpreter.debug("tests/loop.t")