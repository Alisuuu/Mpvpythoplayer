import os
import subprocess
import time
import sys
import termios
import tty
from colorama import init, Fore, Style

# Inicializa o Colorama
init(autoreset=True)

# Configuração da pasta de músicas
MUSIC_DIR = "/storage/emulated/0/Music"

# Função para listar arquivos MP3 na pasta
def find_mp3_files():
    files = []
    for root, _, filenames in os.walk(MUSIC_DIR):
        for file in filenames:
            if file.endswith('.mp3'):
                files.append(os.path.join(root, file))
    return sorted(files)

# Função para formatar o tempo (minutos:segundos)
def format_time(seconds):
    minutes = int(seconds // 60)
    sec = int(seconds % 60)
    return f"{minutes:02}:{sec:02}"

# Função para tocar a música com mpv
def play_music(file_path):
    print(Fore.CYAN + f"\nTocando: {Fore.YELLOW}{os.path.basename(file_path)}\n")
    subprocess.Popen(["mpv", "--no-video", "--force-window=no", "--ao=opensles", file_path])

# Função para capturar entrada de uma tecla sem precisar pressionar Enter
def get_input():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# Função principal do player
def main():
    music_files = find_mp3_files()  # Carregar músicas MP3
    if not music_files:
        print(Fore.RED + "Nenhuma música encontrada em " + MUSIC_DIR)
        return

    index = 0
    while True:
        os.system("clear")  # Limpa a tela
        print(Fore.GREEN + f"\nTocando: {Fore.YELLOW}{os.path.basename(music_files[index])}")
        print(Style.DIM + "\n[←] Anterior  [→] Próxima  [q] Sair")
        
        # Toca a música atual
        play_music(music_files[index])

        # Captura a entrada do usuário
        cmd = get_input()

        # Lógica dos comandos
        if cmd == "←":  # Anterior
            index = (index - 1) % len(music_files)
        elif cmd == "q":  # Sair
            print(Fore.RED + "Saindo do player...")
            break
        elif cmd == "→":  # Próxima
            index = (index + 1) % len(music_files)

        # Verifica se tocou a última música
        if index == len(music_files) - 1:  # Última música
            print(Fore.YELLOW + "Última música tocada.")
            break  # Encerra o player ao final da última música

if __name__ == "__main__":
    main()
    
