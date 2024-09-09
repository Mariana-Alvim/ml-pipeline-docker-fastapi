import boto3
# import psycopg2
import pandas as pd

from service import settings


# Conexão com o banco de dados
def get_db_connection():
    conn = psycopg2.connect(
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT
    )
    return conn

# Função para obter os dados de treinamento e teste
def get_data_from_database(data_db_table_name):
    conn = get_db_connection()
    try:
        query = f"SELECT * FROM {data_db_table_name}"

        df_train = pd.read_sql_query(query, conn)

        return df_train

    finally:
        conn.close()
