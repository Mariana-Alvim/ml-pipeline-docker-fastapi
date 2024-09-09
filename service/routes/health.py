
from fastapi import APIRouter

router = APIRouter()

# Definindo o endpoint de liveness
@router.get("/liveness", tags=["health"], status_code=200)
async def liveness():
    """
    Método liveness.
    """
    return {"status": "Service is alive."}

# Definindo o endpoint de readiness
@router.get("/readiness", tags=["health"], status_code=200)
async def readiness():
    """
    Método readiness
    """
    return {"status": "Service is ready."}
