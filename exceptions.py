class IMError(Exception):
    def __init__ (self, message):
        self.message = message

    def __str__ (self):
        return self.message
    
class BadRequestError(IMError):
    pass

class NoParameterError(IMError):
    pass

class InvalidParameterError(IMError):
    pass

class IllegalStateError(IMError):
    pass

class UnsupportedVersionError(IMError):
    pass
