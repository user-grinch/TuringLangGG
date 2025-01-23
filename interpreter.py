import sys
from filehandler import FileHandler
from parser import Parser
from varstore import VarStore

FILE_NAME :str = 'demo.t'

if __name__ == '__main__':
    # if len(sys.argv) > 1:
    #     print("First argument:", sys.argv[1])

    FileHandler.execute(FILE_NAME);
    Parser.process()
    print(VarStore.getVariables())
