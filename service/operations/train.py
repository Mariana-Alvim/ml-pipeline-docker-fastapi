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

from service.util.upload_model import upload_model


# Pipeline para treinar e avaliar o modelo
def base_model(train: pd.DataFrame, model_name, use_cloud_storage_model):
    train_cols = [
        'type','sector', 'net_usable_area','net_area','n_rooms','n_bathroom','latitude','longitude','price'
        ]
    
    categorical_cols = ["type", "sector"]
    target = "price"
    
    categorical_transformer = TargetEncoder()
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('categorical',
             categorical_transformer,
             categorical_cols)
             ])
    
    steps = [
        ('preprocessor', preprocessor),
        ('model', GradientBoostingRegressor(**{
            "learning_rate":0.01,
            "n_estimators":300,
            "max_depth":5,
            "loss":"absolute_error"
        }))
    ]
    
    pipeline = Pipeline(steps)

    pipeline.fit(train[train_cols], train[target])

    # save model
    joblib.dump(pipeline, './service/models/model.pkl')

    # upload_model
    if use_cloud_storage_model:
        upload_model(model_name)
