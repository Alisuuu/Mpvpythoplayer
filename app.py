import os
import subprocess
import sys
import termios
import tty
from colorama import init, Fore, Style

init(autoreset=True)

MUSIC_DIR = "/storage/emulated/0/Music"

def find_mp3_files():
    files = []
    for root, _, filenames in os.walk(MUSIC_DIR):
        for file in filenames:
            if file.endswith(".mp3"):
                files.append(os.path.join(root, file))
    return sorted(files)

def get_input():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def play_music(file_path):
    return subprocess.Popen(["mpv", "--no-video", "--force-window=no", "--ao=opensles", file_path],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def show_playlist(music_files, current_index):
    print(Fore.CYAN + "\nFaixas encontradas:\n")
    for i, file in enumerate(music_files):
        name = os.path.basename(file)
        if i == current_index:
            print(Fore.GREEN + ">> " + name)
        else:
            print("   " + name)

def main():
    music_files = find_mp3_files()
    if not music_files:
        print(Fore.RED + f"Nenhuma música encontrada em {MUSIC_DIR}")
        return

    index = 0
    current_process = None

    while True:
        os.system("clear")
        show_playlist(music_files, index)
        print(Style.BRIGHT + "\nControles: [←] Anterior  [→] Próxima  [q] Sair\n")

        if current_process and current_process.poll() is None:
            current_process.terminate()

        current_process = play_music(music_files[index])

        cmd = get_input()
        if cmd == "q":
            if current_process and current_process.poll() is None:
                current_process.terminate()
            print(Fore.YELLOW + "Saindo...")
            break
        elif cmd == "→":
            index = (index + 1) % len(music_files)
        elif cmd == "←":
            index = (index - 1) % len(music_files)

if __name__ == "__main__":
    main()
    
