from fastapi import APIRouter
from src.niver65.rest.endpoints import healthcheck_ep, entry_ep, suggestion_ep, load_songs
router = APIRouter()
router.include_router(healthcheck_ep.router)
router.include_router(entry_ep.router)
router.include_router(suggestion_ep.router)
router.include_router(load_songs.router)

