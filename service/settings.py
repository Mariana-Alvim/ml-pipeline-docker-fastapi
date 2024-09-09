import os

"""
    Variaveis booleanas e objetos nao poderao ser definidas nas variaveis de ambiente,
    pois todas serao convertidas para string.
    Para as variaveis definidas com "os.environ.get()" o primeiro valor é referente
    a variavel que está buscando, o segundo valor será usado como valor padrão caso
    não encontre nas variaveis de ambiente.
"""
API_NAME = "Servico API"
VERSION_API = '1.0.1'
TITLE_API = "Predict Price"
DESCRIPTION_API = "API."

API_KEY = os.environ.get('API_KEY')

# FastAPi settings
FLASK_SERVER_NAME = None
FASTAPI_HOST = os.environ.get('FASTAPI_HOST', "0.0.0.0")
FASTAPI_PORT = os.environ.get('FASTAPI_PORT', "5000")
FASTAPI_DEBUG = True  # Do not use debug mode in production

URL_PREFIX = os.environ.get('URL_PREFIX', '')

PATH_LOG = os.environ.get("PATH_LOG", "./log_project_name")
LOG_LEVEL =  os.environ.get("LOG_LEVEL", "DEBUG") # Nível do log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
POOL_CPU = int(os.environ.get("POOL_CPU", os.cpu_count()-1))

# Configurações do banco de dados
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_HOST", "5439") # Porta padrão para PostgreSQL
DB_NAME = os.environ.get("DB_NAME") # Nome do banco de dados
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

LOCAL_FILE = "./service/models/model.pkl"
LOCAL_PATH_DOWNLOAD = "./service/stages/model.pkl"

# Configurações para realizar o upload do modelo no bucket
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
AWS_S3_BUCKET_NAME = os.environ.get("AWS_S3_BUCKET_NAME", "models-predict-price")
AWS_REGION =  os.environ.get("AWS_REGION", "sa-east-1")
