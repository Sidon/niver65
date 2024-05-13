import logging
from abc import ABC
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import HTTPException
from niver65.rest.dto.models_dto import GuestDto
from src.niver65.adapters.models.niver_party_orm import TokenOrm, GuestOrm, SuggestionOrm, SessionsOrm
from src.niver65.adapters.repositories.abstract_repo import AbstractRepository

error_logger = logging.getLogger('error_logger')
info_logger = logging.getLogger('info_logger')

# Repositório para Tokens
class TokenRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, token):
        try:
            self.session.add(token)
            self.session.commit()
        except SQLAlchemyError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get(self, token_id):
        try:
            return self.session.query(TokenOrm).filter_by(token=token_id).one_or_none()
        except SQLAlchemyError as e:
            error_logger.error(f'Erro ao acessar db: {e}')
            raise HTTPException(status_code=500, detail="Erro ao buscar token na base de dados")

    def remove(self, token):
        try:
            self.session.delete(token)
            self.session.commit()
        except SQLAlchemyError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def update_balance(self, token_id: UUID, decrease: int = 1):
        try:
            token_from_db = self.get(token_id)
            token_from_db.balance -= decrease
            self.session.commit()
        except SQLAlchemyError as e:
            raise HTTPException(status_code=400, detail=str(e))


# Repositório para Guests
class GuestRepository(AbstractRepository, ABC):
    def __init__(self, session: Session):
        self.session = session

    def add(self, guest_dto: GuestDto):

        guest_orm = GuestOrm(**guest_dto.dict())
        # breakpoint()
        self.session.add(guest_orm)
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


class SessionsRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, user_session):
        try:
            self.session.add(user_session)
            self.session.commit()
            return user_session  # Após o commit, user_session tem o ID atualizado
        except SQLAlchemyError as e:
            self.session.rollback()  # Importante fazer rollback em caso de falha
            error_logger.error(f'Erro ao acessar db: {e}')
            raise HTTPException(status_code=400, detail=str(e))

    def get(self, session_id):
        try:
            return self.session.query(SessionsOrm).filter_by(id=session_id).one_or_none()
        except SQLAlchemyError as e:
            self.session.rollback()
            error_logger.error(f'Erro ao acessar db: {e}')
            raise HTTPException(status_code=500, detail="Erro ao buscar token na base de dados")

    def remove(self, user_session):
        try:
            self.session.delete(user_session)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise HTTPException(status_code=400, detail=str(e))