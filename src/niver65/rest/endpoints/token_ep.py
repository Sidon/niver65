import logging
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, Request, HTTPException, Form
from fastapi.params import Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from src.niver65.database.db_session import get_db_session
from src.niver65 import settings
from src.niver65.rest.dto import models_dto as dto
from src.niver65.service_layer.guests_service import GuestsService

router = APIRouter()
info_logger = logging.getLogger('info_logger')

@router.get(path=f'{settings.path_base}/', tags=['Entry point'], response_model=dto.ResponseDto)
def entry_point(
        request: Request,
        db_session: Session = Depends(get_db_session),
        token: str = Query(default=None, description="Token do quem recebeu/distribuiu o link")
) -> dto.ResponseDto:
    client_ip = request.client.host
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(",")[0]

    info_logger.info(f'Acesso a / {client_ip}')
    resp = dto.ResponseDto()

    if not token:
        resp.status = 'Falta o token no endereço'
        return resp

    try:
        uuid_token = UUID(token)
    except ValueError:
        resp.status = 'Token inválido'
        return resp

    service_guest = GuestsService(db_session)
    valid_token = service_guest.token_check(uuid_token)

    if valid_token:
        resp.status = valid_token

    return settings.template_jinja2.TemplateResponse("login.html", {"request": request})


@router.post("/check-email", response_class=HTMLResponse)
async def check_email(request: Request, email: str = Form(...)):
    # Aqui, você pode verificar o email e/ou criar uma sessão para o usuário
    # Renderiza a página de sugestão de músicas
    return settings.template_jinja2.TemplateResponse("music_suggestion.html", {"request": request, "email": email})
