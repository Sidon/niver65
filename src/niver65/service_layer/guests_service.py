import logging
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from src.niver65.adapters.repositories.party_repo import TokenRepository, GuestRepository, SuggestionRepository
from src.niver65.rest.dto.models_dto import TokenDto

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
        except SQLAlchemyError as e:
            error_logger.error(f"Erro ao acessar dados no banco: {e}", exc_info=True)

        return None

    def check_login(self, email):
        try:
            guest_orm = self.guest_repo.get(email=email)
            if guest_orm:
                suggestion_orm = self.suggestion_repo.get(email)
                return suggestion_orm
        except SQLAlchemyError as e:
            error_logger.error(f'Erro ao acessr dado do banco: {e}', exc_info=True)

        return None

    def load_suggestions(self):
        return self.suggestion_repo.list_all()
