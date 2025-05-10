import os
import time
import subprocess
from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)

MUSIC_DIR = "/storage/emulated/0/Music"

def find_mp3_files():
    files = []
    for root, _, filenames in os.walk(MUSIC_DIR):
        for file in filenames:
            if file.endswith('.mp3'):
                files.append(os.path.join(root, file))
    return sorted(files)

def format_time(seconds):
    minutes = int(seconds // 60)
    sec = int(seconds % 60)
    return f"{minutes:02}:{sec:02}"

def play_music(file_path):
    print(Fore.CYAN + f"\nTocando: {Fore.YELLOW}{os.path.basename(file_path)}\n")
    subprocess.run(["mpv", "--no-video", "--force-window=no", "--ao=opensles", file_path])

def main():
    music_files = find_mp3_files()
    if not music_files:
        print(Fore.RED + "Nenhuma música encontrada em " + MUSIC_DIR)
        return

    index = 0
    while True:
        os.system("clear")
        disk = ["◴", "◷", "◶", "◵"]
        for i in range(4):
            print(Fore.GREEN + f"\n{disk[i]}  {Fore.MAGENTA}Tocando: {Fore.YELLOW}{os.path.basename(music_files[index])}")
            print(Style.DIM + "\n[Enter] Próxima  [a] Anterior  [q] Sair")
            time.sleep(0.2)
            os.system("clear")

        play_music(music_files[index])

        print(Style.DIM + "\nDigite uma opção:")
        cmd = input("[Enter] próxima | [a] anterior | [q] sair: ").strip().lower()
        if cmd == "a":
            index = (index - 1) % len(music_files)
        elif cmd == "q":
            break
        else:
            index = (index + 1) % len(music_files)

if __name__ == "__main__":
    main()
    
