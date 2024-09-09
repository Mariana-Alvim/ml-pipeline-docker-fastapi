import logging
from loguru import logger
from http import HTTPStatus
from fastapi import APIRouter, Depends, File, UploadFile, Request, Response, Form, HTTPException, Query

from service import settings
from service.responses import objResponse
from service.constants import codeHttp, mensagens
from service.util.veridy_api_key import verify_api_key
from service.util.load_file import load_data
from service.util.get_data_from_database import get_data_from_database
from service.operations.train import base_model

log = logging.getLogger(__name__)

# Inicializando o FastAPI
router = APIRouter()


# Endpoint para receber o arquivo CSV, treinar e salvar o modelo e retornar as métricas de performance do modelo
@router.get("/")
async def root(request:Request, response: Response):
    """
    Método para verificar se o serviço está funcionando.
    """
    try:
        return objResponse.send_success(
            messages="The service is running.",
            data=None,
            status=HTTPStatus.OK.value
        )
    except Exception as e:
        return objResponse.send_exception(
            response,
            objError=e,
            messages="Internal Server Erro",
            status=HTTPStatus.INTERNAL_SERVER_ERROR.value
        )


@router.post("/train")
async def train_model(
    train_file: UploadFile = File(None),
    model_name: str = Form(None),
    train_data_db_table_name: str = Form(None),
    load_file: bool = Query(True),
    use_cloud_storage_model: bool = Query(False),
    api_key: str = Depends(verify_api_key)
    ):
    """
    Método POST para treinar e salvar o modelo treinado.
    """

    logger.debug(mensagens.INICIO_LOAD_SERVICO)

    # Validação dos arquivos, caso o treinamento seja realizado, por meio do carregamento de arquivos
    if load_file:
        if train_file is None:
            raise HTTPException(status_code=400, detail="O arquivo de treino é obrigatório quando o carregamento de arquivos está ativo.")
    
    # Validação do dados necessário para acessar o database, caso o treinamento seja feito por meio dos dados do database
    else:
        if not train_data_db_table_name:
            raise HTTPException(status_code=400, detail="O caminho de acesso aos dados no database é obrigatório quando o carregamento dos arquivos está desativado.")
    
    if use_cloud_storage_model and not model_name:
            raise HTTPException(status_code=400, detail="O nome do modelo é obrigatório para o armazenamento do modelo no bucket.")
    
    if not use_cloud_storage_model:
            model_name = "model"

    try:
        if load_file:
            train_data = load_data(train_file)
        
        else:
            train_data = get_data_from_database(train_data_db_table_name)

        data = base_model(train_data, model_name, use_cloud_storage_model)

        response = objResponse.send_success(
            messages=mensagens.SUCESSO_TREINAMENTO,
            status=codeHttp.SUCCESS_200,
            data={}
            )
        logger.success(mensagens.SUCESSO_TREINAMENTO)
    
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
