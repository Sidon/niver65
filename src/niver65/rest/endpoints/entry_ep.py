import logging
import uuid
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, Request, HTTPException, Form
from fastapi.params import Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from niver65.rest.dto.models_dto import GuestDto
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
    resp = dto.ResponseDto()

    if not token:
        resp.status = 'Falta o token no endereço'
        return resp

    resp.status = 'Token inválido'
    try:
        uuid_token = UUID(token)
    except ValueError:
        return resp

    service_guest = GuestsService(db_session)
    valid_token = service_guest.token_check(uuid_token)

    if valid_token:
        return settings.template_jinja2.TemplateResponse("login.html", {"request": request, "token_id": token})
    else:
        return resp


@router.post("/check-email", response_class=HTMLResponse)
async def process_login(
        request: Request, name: str = Form(...), email: str = Form(...), token_id: UUID = Form(...),
        db_session: Session = Depends(get_db_session),
):
    service_guest = GuestsService(db_session)
    check_login = service_guest.check_login(GuestDto(email=email, name=name, token_id=token_id))

    # Renderiza a página de sugestão de músicas
    return settings.template_jinja2.TemplateResponse(
        "suggest_music.html",
        {
            "request": request,
            "email": email,
            "name": name,
        }
    )

