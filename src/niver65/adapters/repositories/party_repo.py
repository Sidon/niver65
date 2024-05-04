from abc import ABC

from sqlalchemy.orm import Session
from sqlalchemy.future import select

from src.niver65.adapters.models.niver_party_orm import TokenOrm, GuestOrm, SuggestionOrm
from src.niver65.adapters.repositories.abstract_repo import AbstractRepository


# Repositório para Tokens
class TokenRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, token):
        self.session.add(token)
        self.session.commit()

    def get(self, token_id):
        return self.session.query(TokenOrm).filter_by(token=token_id).one_or_none()

    def remove(self, token):
        self.session.delete(token)
        self.session.commit()




# Repositório para Guests
class GuestRepository(AbstractRepository, ABC):
    def __init__(self, session: Session):
        self.session = session

    def add(self, guest):
        self.session.add(guest)
        self.session.commit()

    def get(self, email):
        return self.session.query(GuestOrm).filter_by(email=email).one_or_none()

    def remove(self, guest):
        self.session.delete(guest)
        self.session.commit()


# Repositório para Suggestions
class SuggestionRepository(AbstractRepository, ABC):
    def __init__(self, session: Session):
        self.session = session

    def add(self, suggestion):
        self.session.add(suggestion)
        self.session.commit()

    def get(self, email):
        return self.session.query(SuggestionOrm).filter_by(id_email=email).one_or_none()

    def remove(self, suggestion):
        self.session.delete(suggestion)
        self.session.commit()

    def list_all(self):
        return self.session.query(SuggestionOrm).all()
