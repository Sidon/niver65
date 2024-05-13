import logging
import uuid
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, Request, Form, Cookie, Response, HTTPException
from fastapi.params import Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from niver65.adapters.models.niver_party_orm import SessionsOrm
from niver65.rest.dto.models_dto import GuestDto
from src.niver65 import settings
from src.niver65.rest.dto import models_dto as dto
from src.niver65.database.db_session import get_db_session
from src.niver65.service_layer.guests_service import GuestsService

router = APIRouter()
info_logger = logging.getLogger('info_logger')


@router.get(path=f'{settings.path_base}', tags=['Entry point'], response_model=dto.ResponseDto)
def entry_point(
        request: Request,
        db_session: Session = Depends(get_db_session),
        token: str = Query(default=None, description="Token do quem recebeu/distribuiu o link"),
        uuid_token: str = Cookie(None),
) -> dto.ResponseDto:
    resp = dto.ResponseDto()

    if uuid_token and not token:
        token = uuid_token

    if not token:
        resp.status = 'Falta o token no endereço'
        return resp

    resp.status = 'Token inválido'
    try:
        uuid_token = UUID(token)
    except ValueError:
        return resp

    service_entry = GuestsService(db_session)
    valid_token = service_entry.token_check(uuid_token)
    if valid_token.balance < 1:
        valid_token = None

    if valid_token:
        if valid_token.balance > 0:
            user_session: SessionsOrm = service_entry.create_session_user()
            response = settings.template_jinja2.TemplateResponse("login.html", {"request": request, "token_id": token})
            response.set_cookie(key="user_session", value=user_session.id, httponly=True)
            response.set_cookie(key="uuid_token", value=uuid_token, httponly=True)
            return response

    return resp


@router.post("/process-login", response_class=HTMLResponse)
async def process_login(
        request: Request,
        name: str = Form(...),
        email: str = Form(...),
        token_id: UUID = Form(...),
        db_session: Session = Depends(get_db_session),
):
    service_login = GuestsService(db_session)
    check_login = service_login.check_login(GuestDto(email=email, name=name, token_id=token_id))

    if check_login[0]:
        return settings.template_jinja2.TemplateResponse(
            "suggest_music.html",
            {
                "request": request,
                "email": email,
                "name": name,
                "token_id": token_id,
            }
        )
    else:
        raise HTTPException(status_code=400, detail=check_login[1])
