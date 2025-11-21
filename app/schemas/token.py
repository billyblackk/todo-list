from pydantic import BaseModel


# Schema of what is returned by the API
class Token(BaseModel):
    access_token: str
    token_type: str
