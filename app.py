import os
import subprocess
import sys
import termios
import tty
from colorama import Fore, Style, init

init(autoreset=True)

MUSIC_DIR = "/storage/emulated/0/Music"

def get_mp3_files():
    mp3_files = []
    for root, _, files in os.walk(MUSIC_DIR):
        for f in files:
            if f.endswith(".mp3"):
                mp3_files.append(os.path.join(root, f))
    return sorted(mp3_files)

def show_playlist(playlist, current_index):
    os.system("clear")
    print(Fore.MAGENTA + Style.BRIGHT + "== MP3 PLAYER ==")
    print(Fore.CYAN + "Controles: a = anterior | n = próxima | q = sair\n")
    for i, song in enumerate(playlist):
        name = os.path.basename(song)
        if i == current_index:
            print(Fore.GREEN + ">> " + name)
        else:
            print("   " + name)

def get_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

def play_ffplay(file_path):
    return subprocess.Popen(["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", file_path])

def main():
    playlist = get_mp3_files()
    if not playlist:
        print("Nenhum .mp3 encontrado em", MUSIC_DIR)
        return

    index = 0
    process = None

    while True:
        show_playlist(playlist, index)

        if process:
            process.terminate()

        process = play_ffplay(playlist[index])

        while process.poll() is None:
            key = get_key()
            if key == 'q':
                process.terminate()
                return
            elif key == 'n':
                index = (index + 1) % len(playlist)
                break
            elif key == 'a':
                index = (index - 1) % len(playlist)
                break

if __name__ == "__main__":
    main()
    
