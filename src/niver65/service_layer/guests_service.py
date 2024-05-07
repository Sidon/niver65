import logging
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from starlette.exceptions import HTTPException

from niver65.rest.errors import RestError
from src.niver65.adapters.repositories.party_repo import TokenRepository, GuestRepository, SuggestionRepository
from src.niver65.rest.dto.models_dto import TokenDto, GuestDto

error_logger = logging.getLogger('error_logger')
info_logger = logging.getLogger('info_logger')


class GuestsService:
    def __init__(self, db_session):
        self.token_repo = TokenRepository(db_session)
        self.guest_repo = GuestRepository(db_session)
        self.suggestion_repo = SuggestionRepository(db_session)

    def token_check(self, token):
        try:
            token_orm = self.token_repo.get(token_id=token)
            if token_orm:
                return TokenDto.from_orm(token_orm)
        except HTTPException as http_exc:
            # Aqui você pode retornar a resposta de erro usando o tratamento customizado
            raise http_exc
        except Exception as e:
            # Outros erros inesperados podem ser tratados aqui
            raise RestError(e)

        return None

    def check_login(self, guest: GuestDto):
        try:
            guest_orm = self.guest_repo.get(guest.email)
            if guest_orm:
                suggestion_orm = self.suggestion_repo.get(guest.email)
                return suggestion_orm
            else:
                self.guest_repo.add(guest)
        except SQLAlchemyError as e:
            error_logger.error(f'Erro ao acessr dado do banco: {e}', exc_info=True)

        return None

    def load_suggestions(self):
        return self.suggestion_repo.list_all()
