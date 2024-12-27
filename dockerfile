# Use a imagem base oficial do Python 3.10 slim
FROM python:3.10-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Atualize o gerenciador de pacotes e instale dependências do sistema
RUN apt-get update && apt-get install -y \
    git ffmpeg libsndfile1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Atualize o pip para a versão mais recente
RUN pip install --upgrade pip

# Instale as dependências necessárias
RUN pip install streamlit gtts

# Copie o código da aplicação para o diretório de trabalho
COPY app-gTTS.py .

# Exponha a porta que o Streamlit utilizará
EXPOSE 8505

# Defina a variável de ambiente para permitir que o Streamlit seja acessível externamente
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_PORT=8505

# Comando para rodar a aplicação
CMD ["streamlit", "run", "app-gTTS.py", "--server.port=8505", "--server.address=0.0.0.0"]
