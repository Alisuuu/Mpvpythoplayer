import os
import subprocess
import sys
import termios
import tty
from colorama import init, Fore, Style

init(autoreset=True)

MUSIC_DIR = "/storage/emulated/0/Music"

def find_mp3_files():
    return sorted([
        os.path.join(root, file)
        for root, _, files in os.walk(MUSIC_DIR)
        for file in files if file.endswith(".mp3")
    ])

def get_arrow_input():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch1 = sys.stdin.read(1)
        if ch1 == '\x1b':  # ESC
            ch2 = sys.stdin.read(1)
            if ch2 == '[':
                ch3 = sys.stdin.read(1)
                return ch3  # A=up, B=down, C=right, D=left
        return ch1
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def play_music(path):
    return subprocess.Popen(["mpv", "--no-video", "--ao=opensles", path],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def show_playlist(playlist, current_index):
    os.system("clear")
    print(Fore.MAGENTA + Style.BRIGHT + "== MP3 Player Hacker ==")
    print(Fore.YELLOW + "Use ← (esquerda) / → (direita) para navegar, q para sair.\n")
    for i, track in enumerate(playlist):
        name = os.path.basename(track)
        if i == current_index:
            print(Fore.GREEN + ">> " + name)
        else:
            print("   " + name)

def main():
    playlist = find_mp3_files()
    if not playlist:
        print("Nenhum arquivo MP3 encontrado.")
        return

    index = 0
    current_proc = None

    while True:
        show_playlist(playlist, index)

        if current_proc and current_proc.poll() is None:
            current_proc.terminate()
        current_proc = play_music(playlist[index])

        while True:
            key = get_arrow_input()
            if key == 'q':
                current_proc.terminate()
                return
            elif key == 'C':  # seta para direita
                index = (index + 1) % len(playlist)
                break
            elif key == 'D':  # seta para esquerda
                index = (index - 1) % len(playlist)
                break

if __name__ == "__main__":
    main()
    
