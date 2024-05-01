from sqlalchemy import create_engine, Column, String, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()


class TokenOrm(Base):
    __tablename__ = 'tokens'

    token = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String)

    # Relacionamento com a tabela Guests
    guests = relationship("GuestOrm", back_populates="token")


class GuestOrm(Base):
    __tablename__ = 'guests'

    email = Column(String, primary_key=True)
    name = Column(String)
    token_id = Column(UUID(as_uuid=True), ForeignKey('tokens.token'))

    # Relacionamento com a tabela Tokens e Suggestions
    token = relationship("TokenOrm", back_populates="guests")
    suggestions = relationship("SuggestionOrm", back_populates="guest")


class SuggestionOrm(Base):
    __tablename__ = 'suggestions'

    id = Column(Integer, primary_key=True)
    id_email = Column(String, ForeignKey('guests.email'))
    song_name = Column(String)
    info_song = Column(String)

    # Relacionamento com a tabela Guests
    guest = relationship("GuestOrm", back_populates="suggestions")


