from abc import ABC, abstractmethod

class IBaseInstruction(ABC):
    # Returns the command prefix
    # ie the command name
    @abstractmethod
    def getPrefix() -> str:
        pass

    # This executes the actual command
    # Returns true on success
    @abstractmethod
    def execute(prefix: str, list: list[str]) -> bool:
        pass
