from fastapi import UploadFile
import pandas as pd
import io

# Função para ler o CSV e transformar em DataFrame
def load_data(file: UploadFile):
    content = file.file.read()
    data = pd.read_csv(io.StringIO(content.decode('utf-8')))
    return data