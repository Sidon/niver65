#! /usr/bin/python python3
import logging
import uuid

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from starlette.responses import JSONResponse
from src.niver65.rest.router import router as v1_router
from src.niver65 import settings
from src.niver65.settings import setup_logging
from src.niver65.rest.errors import RestError

# Configurar logs
setup_logging()
info_logger = logging.getLogger('info_logger')

app = FastAPI(
    docs_url=f'{settings.path_base}/docs',
    redoc_url=f'{settings.path_base}/redoc',
    title="Sidon aniversario 2024",
    description="niver65",
    version="v0"
)

app.mount("/static", StaticFiles(directory=settings.static_path), name="static")


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8080/",
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router)


# Evento de inicialização
async def startup():
    info_logger.info("Starting up...")


# Evento de encerramento
async def shutdown():
    info_logger.info("Shutting down...")


# Registrar os eventos
app.router.add_event_handler("startup", startup)
app.router.add_event_handler("shutdown", shutdown)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    request.state.debug_id = str(uuid.uuid4())
    response = await call_next(request)
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return build_error_response(request, exc)


@app.exception_handler(Exception)
async def all_exceptions(request, exc):
    return build_error_response(request, exc)


def build_error_response(request, exc):
    info_logger.exception(exc)
    if not isinstance(exc, RestError):
        exc = RestError(exc, request=request)
    headers = {}
    if exc.headers:
        for header, value in exc.headers.items():
            headers[header] = value
    headers['Content-Type'] = 'application/json'
    return JSONResponse(
        exc.error.dict(),
        headers=headers,
        status_code=exc.statusCode
    )


if __name__ == '__main__':
    uvicorn.run(app,
                host='0.0.0.0',
                port=8000)
