from loguru import logger
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

from service import settings
from service.constants import mensagens


def upload_model(model_name):
    """
    Faz o upload do modelo treinado para um bucket S3.
    """
    logger.debug(mensagens.INICIANDO_UPLOAD_MODEL)

    s3_client = boto3.client(
        service_name='s3',
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY,
        aws_secret_access_key=settings.AWS_SECRET_KEY
    )

    model_name = model_name + ".pkl"

    try:
        s3_client.upload_file(settings.LOCAL_FILE, settings.AWS_S3_BUCKET_NAME, model_name)
        logger.success(mensagens.SUCESSO_UPLOAD)
    
    except NoCredentialsError:
        return "Credenciais não encontradas."
    except PartialCredentialsError:
        return "Credenciais incompletas."
    except Exception as e:
        return f"Erro ao carregar o arquivo: {str(e)}"
