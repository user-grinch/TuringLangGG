class ExceptionBase(Exception):
    def __init__(self, message="ExceptionBase occured"):
        self.message = message
        super().__init__(self.message)