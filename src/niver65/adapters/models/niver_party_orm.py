import datetime

from sqlalchemy import create_engine, Column, String, ForeignKey, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class TokenOrm(Base):
    __tablename__ = 'tokens'
    token = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String)
    limit = Column(Integer)
    balance = Column(Integer)
    guests = relationship("GuestOrm", back_populates="token")  # Relacionamento correto

class GuestOrm(Base):
    __tablename__ = 'guests'
    email = Column(String, primary_key=True)
    name = Column(String)
    token_id = Column(UUID(as_uuid=True), ForeignKey('tokens.token'))  # Nome de coluna mais claro
    token = relationship("TokenOrm", back_populates="guests")  # Relacionamento, não apenas uma coluna
    suggestions = relationship("SuggestionOrm", back_populates="guest")

class SuggestionOrm(Base):
    __tablename__ = 'suggestions'
    id = Column(Integer, primary_key=True)
    id_email = Column(String, ForeignKey('guests.email'))
    song_name = Column(String)
    info_song = Column(String)
    guest = relationship("GuestOrm", back_populates="suggestions")


class SessionsOrm(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    moment = Column(DateTime, default=datetime.datetime)