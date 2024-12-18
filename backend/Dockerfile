# Use uma imagem oficial do Python como imagem base
FROM python:3.9-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Copia o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação para o diretório de trabalho
COPY . .

# Expõe a porta que o Uvicorn vai usar
EXPOSE 8000

# Comando para executar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]