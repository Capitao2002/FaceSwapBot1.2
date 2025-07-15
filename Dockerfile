# Imagem base
FROM python:3.10-slim

# Variáveis
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Instalar dependências de sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos do projeto
COPY . /app

# Instalar dependências Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Clonar o modelo FOMM e preparar diretório de checkpoints
RUN git clone https://github.com/AliaksandrSiarohin/first-order-model first-order-motion-model && \
    mkdir -p first-order-motion-model/checkpoints

# (Opcional) Baixar o checkpoint manualmente ou copiar durante build
# COPY vox-cpk.pth.tar first-order-motion-model/checkpoints/

# Instalar FaceFusion (caso esteja disponível como pacote pip)
RUN pip install facefusion

# Expor a porta da API Flask
EXPOSE 5000

# Comando padrão de inicialização
CMD ["python", "app.py"]