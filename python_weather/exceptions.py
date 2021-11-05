class HTTPException(Exception):
    __slots__ = ('status', 'message', 'response')
    
    def __init__(self, response, error_string: str = None):
        self.status = response.status
        self.message = error_string or f'The server responded with a status of {self.status}'
        self.response = response

        super().__init__(self.message)
    
    def __repr__(self) -> str:
        return f"<HTTPException status={self.status} response={self.response!r}>"
    
    def __int__(self) -> int:
        return self.status
