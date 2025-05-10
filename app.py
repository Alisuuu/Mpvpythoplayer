import os
import sys
import threading
import time
from playsound import playsound
from colorama import Fore

# Caminho correto para músicas no Android
MUSIC_DIR = "/storage/emulated/0/Music"

# Função para buscar todas as músicas .mp3 nas subpastas
def buscar_musicas(diretorio):
    musicas = []
    for root, dirs, files in os.walk(diretorio):
        for file in files:
            if file.lower().endswith(".mp3"):
                musicas.append(os.path.join(root, file))
    return musicas

# Lista todas as músicas no diretório e subdiretórios
playlist = buscar_musicas(MUSIC_DIR)

if not playlist:
    print(Fore.RED + "Nenhuma música .mp3 encontrada em /storage/emulated/0/Music")
    sys.exit()

index = 0
is_playing = True
current_thread = None

def tocar(musica):
    global is_playing
    print(Fore.CYAN + f"Tocando: {musica}")
    playsound(musica)
    is_playing = False

def tocar_em_thread():
    global current_thread, is_playing
    is_playing = True
    current_thread = threading.Thread(target=tocar, args=(playlist[index],), daemon=True)
    current_thread.start()

tocar_em_thread()

while True:
    comando = input(Fore.YELLOW + "[A] Anterior | [N] Próxima | [Q] Sair\n").strip().lower()
    if comando == "q":
        os._exit(0)
    elif comando == "n":
        index = (index + 1) % len(playlist)
        is_playing = False
        time.sleep(0.5)
        tocar_em_thread()
    elif comando == "a":
        index = (index - 1) % len(playlist)
        is_playing = False
        time.sleep(0.5)
        tocar_em_thread()
        
