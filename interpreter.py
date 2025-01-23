import sys
from filehandler import FileHandler
from parser import Parser
from varstore import VarStore

class Interpreter():
    @classmethod
    def run(cls):
        if len(sys.argv) > 1:
            FileHandler.process(sys.argv[1]);
            Parser.process()
            print(VarStore.getVariables())