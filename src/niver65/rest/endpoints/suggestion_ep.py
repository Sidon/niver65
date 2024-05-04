import logging

from fastapi import APIRouter, Depends, Request, HTTPException, Form
from fastapi.params import Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from src.niver65.database.db_session import get_db_session
from src.niver65 import settings
from src.niver65.rest.dto import models_dto as dto
from src.niver65.service_layer.guests_service import GuestsService
from src.niver65.rest.dto.models_dto import ListSuggestionDto, SuggestionDto

router = APIRouter()
info_logger = logging.getLogger('info_logger')


@router.post("/add-music")
async def add_music(
        request: Request,
        music_name: str = Form(...), music_link: str = Form(...),
        db_session: Session = Depends(get_db_session)
):
    # Aqui você adicionaria a música ao banco de dados
    # Retornar a música recém-adicionada para atualização da lista

    music_info = {"song_name": music_name, "song_info": music_link}
    return settings.template_jinja2.TemplateResponse(
        "partials/music_item.html",
        {"request": request, "music": music_info}
    )


@router.get("/load-music", response_model=ListSuggestionDto)
async def load_music(request: Request, db_session: Session = Depends(get_db_session)):
    suggestions_list = []
    service_guest = GuestsService(db_session)
    suggestions_db = service_guest.load_suggestions()
    if suggestions_db:
        suggestions_list = [SuggestionDto.from_orm(sug).dict() for sug in suggestions_db]

    # breakpoint()
    return settings.template_jinja2.TemplateResponse(
         #user_info =
        "partials/all_music_list.html", {"request": request, "music_list": suggestions_list })

