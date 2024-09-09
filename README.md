# Pipeline Automatizado de Treinamento e Avaliação com FastAPI e Docker

Este projeto fornece um pipeline automatizado para treinamento e avaliação de modelos de machine learning de predição de preço de propriedade residencial, servido por meio de uma interface FastAPI e containerizado usando Docker. O pipeline prevê integração contínua para treinamento, avaliação e implantação de modelos.


## Pipeline Automatizado
O pipeline consiste em:

1. **Treinamento do Modelo:** Treina um modelo de machine learning no conjunto de treinamento enviado via endpoint ```/train```.<br><br>
2. **Avaliação do Modelo:** Avalia o modelo treinado no conjunto de teste quando o endpoint ```/evaluate``` é chamado. <br><br>
3. **Predição:** Realiza predições com o modelo treinado usando o endpoint ```/predict```.

*Em cada uma dessas etapas, é necessário fornecer a chave de API.<br>*

*Os dados podem ser enviados carregando um arquivo CSV (mantendo a configuração padrão do parâmetro ```load_file``` como ```True```) ou podem ser utilizados dados do database, informando o nome da tabela de dados e alterando a configuração do parâmetro ```load_file``` como ```False```.<br>*

*Ademais, a imagem Docker contém o modelo padrão utilizado para avaliação e predição. Outros modelos podem ser treinados e armazenados no bucket de nuvem ou acessados para avaliação e predição. Para isto, basta especificar o nome do modelo e alterar a configuração do parâmetro ```use_cloud_storage_model``` para ```True```.*


## Estrutura Geral do Projeto
```bash
├── service/                # Diretório principal do código da aplicação FastAPI
│   ├── app.py              # Arquivo principal que inicializa a API
│   ├── constants/          # Diretório contendo os arquivos de configuração de constantes e mensagens utilizadas na aplicação
│   ├── models/             # Neste diretório é armazenado o modelo treinado
│   ├── operations/         # Contém o scripts das operações de Machine Learning (treinamento, predição e avaliação.)
│   ├── responses/          # Definição de respostas padrão
│   ├── routes/             # Diretório contendo os scripts das rotas da API
│   ├── stages/             # Armazena o arquivo do modelo treinado obtido por meio do download do armazenamento em nuvem
│   ├── utils/              # Diretório contendo scripts das funções utilitárias (upload do modelo, obtenção de dados do database, etc.)
│   ├── __init__.py         # Inicializa o módulo do serviço
│   ├── __main__.py         # Script principal para rodar a aplicação FastAPI, configurando o servidor
│   ├── logging.conf        # Arquivo de configuração do logging, definindo níveis de log e formatação
│   └── settings.py         # Configurações da aplicação, como paths e parâmetros de execução
├── .env                    # Arquivo contendo variáveis de ambiente (por exemplo, credenciais do DB para teste local)
├── docker-compose.yml      # Define a configuração de serviços Docker para a aplicação
├── Dockerfile.dev          # Dockerfile para construir a imagem Docker da aplicação
├── log_project_name        # Diretório ou arquivo de logs específicos para monitorar o projeto
├── README.md               # Este arquivo
├── requirements.txt        # Arquivo com as dependências de bibliotecas Python necessárias para o projeto
└── setup.py                # Script de configuração do pacote Python, listando metadados e opções de instalação

```


## Funcionalidades da API

| **Endpoint** | **Método HTTP** | **Descrição** | **Parâmetros** |
|--------------|-----------------|---------------|----------------|
| `/` | `GET` | Verifica o estado geral da API. | Nenhum |
| `/train` | `POST` | Inicia o processo de treinamento de um modelo de Machine Learning com os dados fornecidos. O retorno inclui o status do treinamento. <br><br> **Origem dos dados**: os dados podem ser fornecidos por um arquivo *.csv* ou especificando o nome da tabela no banco de dados. Utilize o parâmetro booleano `load_file` para configurar a origem dos dados (padrão: `True`, para arquivo). <br><br> **Armazenamento em nuvem**: opcionalmente, o modelo treinado pode ser salvo em um bucket de armazenamento na nuvem. O parâmetro booleano `use_cloud_storage_model` está definido como `True` por padrão, para salvar automaticamente o modelo. | **Cabeçalhos com a chave de API** <br> ```headers = {'api-key': api_key}``` <br><br> **Dados do formulário** <br> ```data = {'load_file': 'True', 'use_cloud_storage_model': 'False', 'model_name': 'str', 'train_data_db_table_name': 'str'}``` <br><br> **Arquivo** <br> ```files = {'train_file': open(csv_file_path, 'rb')}``` |
| `/evaluate` | `POST` | Avalia o modelo treinado utilizando um conjunto de dados de teste, retornando as métricas de performance, como: <br> - **RMSE** (*Root Mean Squared Error*): raiz quadrada da média dos erros quadrados; <br> - **MAPE** (*Mean Absolute Percentage Error*): média percentual dos erros absolutos; <br> - **MAE** (*Mean Absolute Error*): média dos erros absolutos. | **Cabeçalhos com a chave de API** <br> ```headers = {'api-key': api_key}``` <br><br> **Dados do formulário** <br> ```data = {'load_file': 'True', 'use_cloud_storage_model': 'False', 'model_name': 'str', 'test_data_db_table_name': 'str'}``` <br><br> **Arquivo** <br> ```files = {'test_file': open(csv_file_path, 'rb')}``` |
| `/predict` | `POST` | Gera previsões para novos dados utilizando o modelo de Machine Learning treinado e retorna um arquivo CSV com as predições realizadas.| **Cabeçalhos com a chave de API** <br> ```headers = {'api-key': api_key}``` <br><br> **Dados do formulário** <br> ```data = {'load_file': 'True', 'use_cloud_storage_model': 'False', 'model_name': 'str', 'data_db_table_name': 'str'}``` <br><br> **Arquivo** <br> ```files = {'data_file': open(csv_file_path, 'rb')}``` |
| `/liveness` | `GET` | Verifica a "vivacidade" da API, confirmando se ela está ativa e respondendo adequadamente. Retorna uma mensagem simples indicando se a API está funcionando.| Nenhum |
| `/readiness` | `GET` | Verifica se a API está pronta para processar requisições, garantindo que os serviços necessários estejam operacionais. Retorna uma mensagem indicando se a API está pronta para o processar requisições. | Nenhum |

- **Método HTTP**: Define o método HTTP utilizado para chamar o endpoint (`GET`, `POST`, `PUT`, `DELETE`).
- **Descrição**: Breve explicação sobre a funcionalidade do endpoint.
- **Parâmetros**: Indica os parâmetros esperados na requisição.


## Pré-requisitos

1. **Docker** instalado.
2. **Python 3.10** se desejar rodar localmente sem Docker.


## Instruções de Configuração

### 1. Construção da Imagem Docker
```bash
docker compose build
```
### 2. Execução do Container Docker
```bash
docker compose up
```

### 3. Accesso à API
Ao executar o container, é possível acessar a API em ```http://localhost:5000```

### 4. Documentação da API
O acesso à documentação da API estará disponível por meio endereço: ```http://localhost:5000/docs```.


## Desenvolvimento local (sem Docker)

### 1. Instalação as dependências
```bash
pip install -U -r requirements.txt
```

### 2. Execução FastAPI localmente
```bash
python -m uvicorn service.app:app --reload
```

### 3. Accesso à API
Acesse a API em ```http://localhost:8000```.

### 4. Documentação da API
O acesso à documentação da API estará disponível por meio endereço: ```http://localhost:8000/docs```.


## Melhorias Futuras
- Implementar deploy contínuo usando CI/CD.
- Adicionar testes unitários para os endpoints da API.
