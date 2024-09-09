from loguru import logger
from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form, Query
from fastapi.responses import StreamingResponse
import io
import pandas as pd
from typing import Optional

from service import settings
from service.responses import objResponse
from service.constants import codeHttp, mensagens
from service.util.veridy_api_key import verify_api_key
from service.util.load_file import load_data
from service.util.get_data_from_database import get_data_from_database
from service.operations.predict import predict_price


# Inicializando o FastAPI
router = APIRouter()

# Endpoint para receber o arquivo CSV e retornar as métricas de performance do modelo
@router.post("/predict")
async def predict(
    data_file: UploadFile = File(None), 
    model_name: str = Form(None),
    load_file: bool = Query(True),
    data_db_table_name: str = Form(None), 
    use_cloud_storage_model: bool = Query(False),
    api_key: str = Depends(verify_api_key)):
    """
    Método POST para treinar e salvar o modelo treinado.
    """
    logger.debug(mensagens.INICIO_PREDICAO)

    if load_file:
        if data_file is None:
            raise HTTPException(status_code=400, detail="O arquivo de dados é obrigatório quando o carregamento de arquivo está ativo.")
    
    # Validação do dados necessário para acessar o database, caso o treinamento seja feito por meio dos dados do database
    else:
        if not data_db_table_name:
            raise HTTPException(status_code=400, detail="O caminho de acesso aos dados no database é obrigatório quando o carregamento dos arquivos está desativado.")
    
    if use_cloud_storage_model and not model_name:
        raise HTTPException(status_code=400, detail="O nome do modelo é obrigatório para o download do modelo do bucket.")
    
    if not use_cloud_storage_model:
        model_name = "model"

    try:
        if load_file:
            data = load_data(data_file)
        
        else:
            data = get_data_from_database(data_db_table_name)

        predicoes = predict_price(data, model_name, use_cloud_storage_model)

        df_predicoes = pd.DataFrame(
            {
                "Predicted price": predicoes
            })
        
        # Utilizando vírgula como separador de milhares
        df_predicoes['Predicted price'] = df_predicoes['Predicted price'].map(lambda x: str(x).replace('.', ','))

        # Usando StringIO para gerar o CSV em memória
        stream = io.StringIO()
        df_predicoes.to_csv(stream, index = False, sep=",", float_format='%.12f')

        response=StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=export.csv"
        logger.success(mensagens.SUCESSO_PREDICAO)
    
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
