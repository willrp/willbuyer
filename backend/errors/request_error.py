from .error import Error


class RequestError(Error):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message


class ValidationError(RequestError):
    def __init__(self, message):
        super().__init__(message)
