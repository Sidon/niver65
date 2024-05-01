import logging
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from src.niver65.adapters.repositories.party_repo import TokenRepository
from src.niver65.rest.dto.models_dto import TokenDto

error_logger = logging.getLogger('error_logger')
info_logger = logging.getLogger('info_logger')


class GuestsService:
    def __init__(self, db_session):
        self.token_repo = TokenRepository(db_session)

    def token_check(self, token):
        try:
            token_orm = self.token_repo.get(token_id=token)
            return TokenDto.from_orm(token_orm)
        except SQLAlchemyError as e:
            error_logger.error(f"Erro ao acessar dados no banco: {e}", exc_info=True)

        return None
