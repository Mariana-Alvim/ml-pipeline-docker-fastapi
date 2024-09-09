import sys
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger

from service import settings
from service.constants import codeHttp, mensagens
from service.routes import train_model, evaluate_model, predict_price, health

app = FastAPI(
    title="API de Predição de Custos",
    docs_url="/docs",
    openapi_url="/docs/openapi.json",
    version="1.0.1"
)

app.include_router(train_model.router)
app.include_router(evaluate_model.router)
app.include_router(predict_price.router)
app.include_router(health.router)


logger.configure(
    handlers=[
        {
            "sink": sys.stdout,
            "level": settings.LOG_LEVEL
        }
    ]
)

logger.add(settings.PATH_LOG)

# Handler de erro global
@app.exception_handler(Exception)
async def default_error_handler(request: Request, exc: Exception):
    logger.exception(mensagens.ERROR_NOT_TREATMENT)

    if not settings.FASTAPI_DEBUG:
        return JSONResponse(
            content={"mensagem": mensagens.ERROR_NOT_TREATMENT},
            status_code=codeHttp.ERROR_500
        )

