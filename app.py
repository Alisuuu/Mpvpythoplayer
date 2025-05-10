import os
import subprocess
import time

# Função para buscar todas as músicas .mp3 no diretório e subdiretórios
def buscar_musicas(diretorio):
    musicas = []
    # Percorre todos os diretórios e subdiretórios
    for root, dirs, files in os.walk(diretorio):
        for file in files:
            # Verifica se o arquivo tem extensão .mp3
            if file.lower().endswith(".mp3"):
                musicas.append(os.path.join(root, file))
    return musicas

# Função para tocar a música usando mpv
def tocar_musica(musica):
    # Executa o mpv com o arquivo de música
    process = subprocess.Popen(['mpv', '--no-terminal', '--loop', musica])
    return process

# Função para parar a música atual
def parar_musica(process):
    process.terminate()  # Encerra o processo do mpv
    time.sleep(1)  # Dá tempo para o mpv terminar a execução

# Função para controlar a próxima música
def tocar_proxima(lista_musicas, indice_atual):
    indice_atual += 1
    if indice_atual >= len(lista_musicas):
        indice_atual = 0  # Retorna para a primeira música
    return indice_atual

# Função para controlar a música anterior
def tocar_anterior(lista_musicas, indice_atual):
    indice_atual -= 1
    if indice_atual < 0:
        indice_atual = len(lista_musicas) - 1  # Vai para a última música
    return indice_atual

# Função principal
def main():
    # Caminho da pasta onde estão as músicas (ajuste para o seu diretório)
    MUSIC_DIR = "/storage/emulated/0/Music"
    
    # Busca as músicas
    musicas = buscar_musicas(MUSIC_DIR)
    
    if not musicas:
        print("Nenhuma música encontrada na pasta.")
        return
    
    # Exibe as músicas encontradas
    print("Músicas encontradas:")
    for i, musica in enumerate(musicas):
        print(f"{i+1}. {musica}")
    
    # Começa a tocar a primeira música
    indice_atual = 0
    process = tocar_musica(musicas[indice_atual])

    while True:
        comando = input("\nComandos: [n] Próxima | [p] Anterior | [q] Sair: ").strip().lower()
        
        if comando == 'n':
            parar_musica(process)  # Para a música atual
            indice_atual = tocar_proxima(musicas, indice_atual)
            process = tocar_musica(musicas[indice_atual])  # Toca a próxima música
        elif comando == 'p':
            parar_musica(process)  # Para a música atual
            indice_atual = tocar_anterior(musicas, indice_atual)
            process = tocar_musica(musicas[indice_atual])  # Toca a música anterior
        elif comando == 'q':
            print("Saindo do player...")
            parar_musica(process)  # Para a música atual
            break
        else:
            print("Comando inválido. Tente novamente.")

if __name__ == "__main__":
    main()
    
