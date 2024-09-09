import logging
from loguru import logger
from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException, Query
# from starlette.requests import Request

from service import settings
from service.responses import objResponse
from service.constants import codeHttp, mensagens
from service.util.veridy_api_key import verify_api_key
from service.util.load_file import load_data
from service.util.get_data_from_database import get_data_from_database
from service.operations.evaluate import evaluate

log = logging.getLogger(__name__)

# Inicializando o FastAPI
router = APIRouter()


# Endpoint para receber o arquivo CSV e avaliar o modelo, retornando as métricas de performance do mesmo.
@router.post("/evaluate", summary="Evaluate model")
async def train_model(
    test_file: UploadFile = File(None),
    model_name: str = Form(None),
    test_data_db_table_name: str = Form(None),
    load_file: bool = Query(True),
    use_cloud_storage_model: bool = Query(False),
    api_key: str = Depends(verify_api_key)
    ):
    """
    Método POST para avaliar modelo treinado.
    """

    logger.debug(mensagens.INICIO_AVALIACAO)

    # Validação dos arquivos, caso o treinamento seja realizado, por meio do carregamento de arquivos
    if load_file:
        if test_file is None:
            raise HTTPException(status_code=400, detail="O arquivo de teste é obrigatório quando o carregamento de arquivo está ativo.")
    
    # Validação do dados necessário para acessar o database, caso o treinamento seja feito por meio dos dados do database
    else:
        if not test_data_db_table_name:
            raise HTTPException(status_code=400, detail="O caminho de acesso aos dados no database é obrigatório quando o carregamento dos arquivos está desativado.")
    
    if use_cloud_storage_model and not model_name:
        raise HTTPException(status_code=400, detail="O nome do modelo é obrigatório para o download do modelo do bucket.")
    
    if not use_cloud_storage_model:
        model_name = "model"

    try:
        if load_file:
            test_data = load_data(test_file)
        
        else:
            test_data = get_data_from_database(test_data_db_table_name)

        data = evaluate(test_data, model_name, use_cloud_storage_model)

        response = objResponse.send_success(
            messages=mensagens.SUCESSO_AVALIACAO,
            status=codeHttp.SUCCESS_200,
            data=data
            )
        logger.success(mensagens.SUCESSO_AVALIACAO)
    
    except OSError as error:
        response = objResponse.send_exception(objError=error, messages=mensagens.ERROR_OS, status=codeHttp.ERROR_500)
        logger.error(mensagens.ERROR_NONE_TYPE)

    except TypeError as error:
        response = objResponse.send_exception(objError=error, messages=mensagens.ERROR_NONE_TYPE, status=codeHttp.ERROR_500)
        logger.error(mensagens.ERROR_NONE_TYPE)

    except Exception as error:
        response = objResponse.send_exception(objError=error, messages=mensagens.ERROR_GENERIC, status=codeHttp.ERROR_500)
        logger.error(error)

    return response
