from fastapi import HTTPException

class UserNotFound(HTTPException):
    def __init__(self, detail: str = "User not found"):
        super().__init__(status_code=404, detail=detail)

class InvalidData(HTTPException):
    def __init__(self, detail: str = "Invalid data provided"):
        super().__init__(status_code=400, detail=detail)

class DatabaseError(HTTPException):
    def __init__(self, detail: str = "An error occurred while accessing the database"):
        super().__init__(status_code=500, detail=detail)

class PostNotFound(HTTPException):
    def __init__(self, detail: str = "Post not found"):
        super().__init__(status_code=404, detail=detail)

class CommentNotFound(HTTPException):
    def __init__(self, detail: str = "Comment not found"):
        super().__init__(status_code=404, detail=detail)

class LikeNotFound(HTTPException):
    def __init__(self, detail: str = "Like not found"):
        super().__init__(status_code=404, detail=detail)