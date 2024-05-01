from fastapi import APIRouter
from src.niver65.rest.endpoints import token_ep, healthcheck_ep
router = APIRouter()
router.include_router(token_ep.router)
router.include_router(healthcheck_ep.router)
