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
            print(VarStore.getVariables())