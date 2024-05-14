import logging
from uuid import UUID
from fastapi import APIRouter, Depends, Request, HTTPException, Form, status, Cookie
from fastapi.openapi.models import Response
from fastapi.responses import Response
from starlette.responses import JSONResponse
from starlette.status import HTTP_302_FOUND
from sqlalchemy.orm import Session

from niver65.adapters.models.niver_party_orm import SuggestionOrm
from src.niver65.database.db_session import get_db_session
from src.niver65 import settings
from src.niver65.service_layer.guests_service import GuestsService
from src.niver65.rest.dto.models_dto import ListSuggestionDto, SuggestionDto
from src.niver65.adapters.repositories.party_repo import SuggestionRepository, TokenRepository

router = APIRouter()
info_logger = logging.getLogger('info_logger')
suggestions = []


@router.post("/add-music")
async def add_music(
        request: Request,
        music_name: str = Form(...),
        music_link: str = Form(...),
        email_id: str = Form(...),
        action: str = Form(...),
        token_id: UUID = Form(...),
        user_session: str = Cookie(None),
        db_session: Session = Depends(get_db_session),
):
    # breakpoint()

    if not user_session:
        response = JSONResponse(status_code=HTTP_302_FOUND, content={})
        response.headers['HX-Redirect'] = '/'
        return response

    if email_id and music_name and music_link:
        suggestions.append(SuggestionDto(id_email=email_id, song_name=music_name, info_song=music_link))

    # breakpoint()
    if action == 'conclude':
        redirect = '/goodbye'
        if len(suggestions) > 0:
            sugg_repo = SuggestionRepository(db_session)
            tk_repo = TokenRepository(db_session)
            for sugg_dto in suggestions:
                sugg_orm = SuggestionOrm(**sugg_dto.dict())
                token_from_db = tk_repo.get(token_id)

                if token_from_db.balance > 0:
                    sugg_repo.add(sugg_orm)
                    tk_repo.update_balance(token_id)
                else:
                    redirect = '/good-max'
                    break

            response = JSONResponse(status_code=HTTP_302_FOUND, content={})
            response.headers['HX-Redirect'] = redirect
            return response

    if action == 'cancel':
        response = JSONResponse(status_code=HTTP_302_FOUND, content={},)
        response.headers['HX-Redirect'] = '/goodbye'
        return response

    music_obj = {"song_name": music_name, "song_link": music_link}
    return settings.template_jinja2.TemplateResponse(
        "partials/music_item.html",
        {"request": request, "music": music_obj}
    )


@router.get("/load-music", response_model=ListSuggestionDto)
async def load_music(request: Request, db_session: Session = Depends(get_db_session)):
    suggestions_list = []
    service_guest_sugg = GuestsService(db_session)
    suggestions_db = service_guest_sugg.load_suggestions()
    if suggestions_db:
        suggestions_list = [SuggestionDto.from_orm(sug).dict() for sug in suggestions_db]

    # breakpoint()
    return settings.template_jinja2.TemplateResponse(
        "partials/all_music_list.html", {"request": request, "music_list": suggestions_list})


@router.get("/goodbye")
async def goodbye(request: Request, response: Response):
    response = settings.template_jinja2.TemplateResponse("goodbye.html", {"request": request})

    response.delete_cookie(key="user_session")
    return response


@router.get("/good-max")
async def goodbye(request: Request, response: Response):
    response = settings.template_jinja2.TemplateResponse("good_max.html", {"request": request})

    response.delete_cookie(key="user_session")
    return response
