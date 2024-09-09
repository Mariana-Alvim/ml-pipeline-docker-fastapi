import joblib

from service import settings

def load_model(use_cloud_storage_model):
    # load
    if use_cloud_storage_model:
        with open(settings.LOCAL_PATH_DOWNLOAD, 'rb') as f:
            model = joblib.load(f)
    else:
        with open(settings.LOCAL_FILE, 'rb') as f:
            model = joblib.load(f)

    return model