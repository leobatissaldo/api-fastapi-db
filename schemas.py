from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    email: str
    senha: str

class UsuarioOutput(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

class TokenOutput(BaseModel):
    access_token: str
    token_type: str