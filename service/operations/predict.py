from loguru import logger

from service.constants import mensagens
from service.util.download_model import download_model
from service.util.load_model import load_model


def predict_price(data, model_name, use_cloud_storage_model):

    if use_cloud_storage_model:
        download_model(model_name)

    logger.debug(mensagens.CARREGANDO_MODELO)
    model = load_model(use_cloud_storage_model)
    
    logger.debug("Iniciando as predições...")
    predicoes = model.predict(data)

    return predicoes
