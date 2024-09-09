from loguru import logger
import pandas as pd
import numpy as np

from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_percentage_error,
    mean_absolute_error)

from category_encoders import TargetEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
import joblib

from service.constants import mensagens
from service.util.download_model import download_model
from service.util.load_model import load_model

def metrics(predictions, target):
    metrics = {
        "RMSE": np.sqrt(mean_squared_error(predictions, target)),
         "MAPE":  mean_absolute_percentage_error(predictions, target),
        "MAE": mean_absolute_error(predictions, target)
        }
    return metrics

# Avaliação do modelo
def evaluate(test: pd.DataFrame, model_name, use_cloud_storage_model):
    if use_cloud_storage_model:
        download_model(model_name)
    
    logger.debug(mensagens.CARREGANDO_MODELO)
    model = load_model(use_cloud_storage_model)

    train_cols = [
        'type','sector', 'net_usable_area','net_area','n_rooms','n_bathroom','latitude','longitude','price'
        ]
    target = "price"
    
    test_predictions = model.predict(test[train_cols])
    test_target = test[target].values

    return metrics(test_predictions, test_target)
