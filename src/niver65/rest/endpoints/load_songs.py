from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from src.niver65.database.db_session import get_db_session
from src.niver65 import settings
from src.niver65.service_layer.guests_service import GuestsService
from src.niver65.rest.dto.models_dto import SuggestionDto

router = APIRouter()


@router.get("/all-songs")
async def show_all_music_data(request: Request, db_session: Session = Depends(get_db_session)):
    suggestions_list = []
    service_guest_sugg = GuestsService(db_session)
    suggestions_db = service_guest_sugg.load_suggestions()
    if suggestions_db:
        suggestions_list = [SuggestionDto.from_orm(sug).dict() for sug in suggestions_db]

    return settings.template_jinja2.TemplateResponse(
        "show_all_music.html", {"request": request, "music_list": suggestions_list})
