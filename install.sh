#!/data/data/com.termux/files/usr/bin/bash

# Atualizar e instalar dependências
pkg update -y && pkg upgrade -y && pkg install -y git python ffmpeg mpv curl

# Clonar o repositório
git clone https://github.com/Alisuuu/Mpvpythoplayer.git

# Acessar o diretório do repositório
cd Mpvpythoplayer

# Instalar as dependências do Python
pip install -r requirements.txt

# Executar o player
python app.py
