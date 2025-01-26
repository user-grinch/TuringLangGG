from exceptions.ibase import ExceptionBase

class IOException(ExceptionBase):
    def __init__(self, message="IOException occured"):
        self.message = message
        super().__init__(self.message)

class UnknownIdentifierException(ExceptionBase):
    def __init__(self, name, message="UnknownIdentifierException occured"):
        self.name = name
        self.message = message
        super().__init__(self.message)

class TypeConversionException(ExceptionBase):
    def __init__(self, required, current, message="TypeConversionException occured"):
        self.current = current
        self.required = required
        self.message = message
        super().__init__(self.message)
        
class UnknownInstructionException(ExceptionBase):
    def __init__(self, name, message="UnknownInstructionException occured"):
        self.name = name
        self.message = message
        super().__init__(self.message)