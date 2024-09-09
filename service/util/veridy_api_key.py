
from fastapi import Header, HTTPException
# from starlette.requests import Request

from service import settings
from service.constants import mensagens


def verify_api_key(api_key: str = Header(...)):
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail=mensagens.ERROR_KEY)