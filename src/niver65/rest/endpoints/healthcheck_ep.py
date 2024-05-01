import logging
from fastapi import APIRouter, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.niver65 import settings
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from src.niver65.rest.dto.erros_dto import ResponseError
# Inicializando o router para este endpoint específico
router = APIRouter()

# Rota para o health check
health_route = f'{settings.path_base}/{settings.health_path}'

# Headers padrões para as respostas JSON
objHeaders = {'Accept': 'application/json', 'Content-Type': 'application/json'}
health_message='''Retorna uma mensagem simples dizendo que serviço está disponível'''
get_health_check = {200: {"model": None, "description": health_message},
                       500: {"model": ResponseError, "description": HTTP_500_INTERNAL_SERVER_ERROR}
                       }


@router.get(health_route, tags=["Sistema"], status_code=HTTP_200_OK, responses={**get_health_check},
            description='API utilizada para validar o status atual da aplicação')
async def get_healthcheck() -> Response:
    content = ['STATUS UP']
    json_compatible_item_data = jsonable_encoder(content)
    return JSONResponse(status_code=HTTP_200_OK, content=json_compatible_item_data, headers=objHeaders)
