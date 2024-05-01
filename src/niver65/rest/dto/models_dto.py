from pydantic import BaseModel, EmailStr, constr
from typing import List, Optional
from uuid import UUID


# Modelo Pydantic para Token
class TokenDto(BaseModel):
    token: UUID
    nome: str

    class Config:
        from_attributes = True


# Modelo Pydantic para Guest
class GuestDto(BaseModel):
    email: EmailStr
    name: str
    token_id: UUID

    class Config:
        from_attributes = True


# Modelo Pydantic para Suggestion
class SuggestionDto(BaseModel):
    id: int
    id_email: EmailStr
    song_name: str
    info_song: Optional[str]

    class Config:
        from_attributes = True


# Modelo Pydantic adicional para resposta detalhada
class GuestDetailDto(GuestDto):
    suggestions: List[SuggestionDto] = []

    class Config:
        from_attributes = True


class ResponseDto(BaseModel):
    status: Optional[str] = None
