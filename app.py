import os
import sys
import threading
import time
from playsound import playsound
from colorama import Fore

MUSIC_DIR = "/sdcard/Music"

playlist = [f for f in os.listdir(MUSIC_DIR) if f.lower().endswith(".mp3")]
if not playlist:
    print(Fore.RED + "Nenhuma música .mp3 encontrada em /sdcard/Music")
    sys.exit()

index = 0
is_playing = True
current_thread = None

def tocar(musica):
    global is_playing
    print(Fore.CYAN + f"Tocando: {musica}")
    playsound(os.path.join(MUSIC_DIR, musica))
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
        
