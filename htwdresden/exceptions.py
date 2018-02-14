class HTWBaseException(Exception):
    pass


class HTWAuthenticationException(HTWBaseException):
    pass


class HTWRequestException(HTWBaseException):
    pass


class HTWServerException(HTWBaseException):
    pass
