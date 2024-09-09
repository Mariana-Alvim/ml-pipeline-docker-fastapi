import uvicorn
from service.app import app
from service import settings


def start():
    uvicorn.run(app, host=settings.FASTAPI_HOST, port=settings.FASTAPI_PORT, debug=settings.FASTAPI_DEBUG)
    print(__package__, ' started.')


if __name__ == '__main__':
    start()
