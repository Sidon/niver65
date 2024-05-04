from fastapi import APIRouter
from src.niver65.rest.endpoints import healthcheck_ep, entry_ep, suggestion_ep
router = APIRouter()
router.include_router(healthcheck_ep.router)
router.include_router(entry_ep.router)
router.include_router(suggestion_ep.router)

