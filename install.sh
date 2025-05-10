#!/data/data/com.termux/files/usr/bin/bash

# Atualizar e instalar dependências
pkg update -y && pkg upgrade -y
pkg install git nodejs -y

# Clonar o repositório
git clone https://github.com/SEU_USUARIO/seu-repositorio.git

# Acessar a pasta do repositório
cd seu-repositorio

# Instalar dependências do projeto
npm install

# Rodar o player
npm start
