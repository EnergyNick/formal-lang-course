
class InterpreterException(Exception):
    pass


class IncorrectVariableException(Exception):
    def __init__(self, variable_name: str):
        self.message = f'Can\'t use undefined variable \"{variable_name}\"'
        super().__init__(self.message)


class InvalidOperationStateException(InterpreterException):
    def __init__(self, incorrect_value, operation: str):
        self.message = f'Type {type(incorrect_value)} is not valid for \"{operation}\" operation'
        super().__init__(self.message)


class InvalidArgumentPlaceException(InterpreterException):
    def __init__(self, operation: str):
        self.message = f'Too more arguments for \"{operation}\" operation'
        super().__init__(self.message)


class InvalidGroupOperationException(InterpreterException):
    def __init__(self, val1, val2, operation: str):
        self.message = f'Can\'t match types {type(val1)} with {type(val2)} for \"{operation}\" operation'
        super().__init__(self.message)
