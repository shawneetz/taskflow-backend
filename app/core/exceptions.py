# Custom HTTP exceptions
from fastapi import HTTPException, status

class NotFoundException(HTTPException):
    def __init__(self, entity: str = "Resources"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f"{entity} not found")

class ForbiddenException(HTTPException):
    def __init__(self):
        super(). init(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden")

class ConflictException(HTTPException):
    def __init__(self, detail:str):
        super.__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers={"WWW-Authenticate": "Bearer"},)