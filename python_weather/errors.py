class Error(Exception):
    __slots__ = ("__message",)

    def __init__(self, message: str):
        self.__message = message

        super().__init__(message)

    def __repr__(self):
        """Returns the string representation of the error."""

        return f'<Error "{self.__message}">'

    def __str__(self) -> str:
        """Returns the error message."""

        return self.__message


class InvalidArg(Error):
    __slots__ = ("got", "expected", "__message")

    def __init__(self, expected, got):
        self.expected = expected
        self.got = got
        self.__message = f"Expected {expected!r}, got {got!r}"

        super().__init__(self.__message)

    def __repr__(self) -> str:
        """Returns the string representation of the error."""

        return f"<InvalidArg expected={self.expected!r} got={self.got!r}>"

    def __str__(self) -> str:
        """Returns the error message."""

        return self.__message
