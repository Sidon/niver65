import logging

from fastapi import Cookie
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from starlette.exceptions import HTTPException

from niver65.adapters.models.niver_party_orm import SessionsOrm, GuestOrm
from niver65.rest.errors import RestError
from src.niver65.adapters.repositories.party_repo import TokenRepository, GuestRepository, SuggestionRepository, \
    SessionsRepository
from src.niver65.rest.dto.models_dto import TokenDto, GuestDto, SessionsDto
from src.niver65.database.db_session import get_db_session

error_logger = logging.getLogger('error_logger')
info_logger = logging.getLogger('info_logger')


class GuestsService:
    def __init__(self, db_session):
        self.token_repo = TokenRepository(db_session)
        self.guest_repo = GuestRepository(db_session)
        self.suggestion_repo = SuggestionRepository(db_session)
        self.user_session_repo = SessionsRepository(db_session)

    def token_check(self, token):
        try:
            token_orm = self.token_repo.get(token_id=token)
            if token_orm:
                return TokenDto.from_orm(token_orm)
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise (e)

        return None

    def check_login(self, guest: GuestDto):
        try:
            guest_orm: GuestOrm = self.guest_repo.get(guest.email)
            if not guest_orm:
                self.guest_repo.add(guest)
                return True, "Novo convidado"
            if guest_orm.token_id != guest.token_id:
                return False, "Token inválido"
        except SQLAlchemyError as e:
            error_logger.error(f'Erro ao acessar dado do banco: {e}', exc_info=True)
        return True, "Ok, Convidado encontrado"

    def load_suggestions(self):
        return self.suggestion_repo.list_all()

    def create_session_user(self):
        user_session_dto = SessionsDto()
        user_session_orm = SessionsOrm(**user_session_dto.dict())
        return self.user_session_repo.add(user_session_orm)


