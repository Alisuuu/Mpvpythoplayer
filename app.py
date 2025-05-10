import os
import sys
import time
import random
import mpv
import itertools
from pathlib import Path
from colorama import Fore, Style, init

# Inicializa colorama
init(autoreset=True)

# Configurações
MUSIC_FOLDER = "/storage/emulated/0/Music"
HISTORY_FILE = os.path.expanduser("~/.music_history")
PLAYLIST_FILE = os.path.expanduser("~/.current_playlist")

spinner = itertools.cycle(['|', '/', '-', '\\'])
colors = [Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.YELLOW]

def format_time(seconds):
    return time.strftime('%M:%S', time.gmtime(seconds or 0))

def render_disc(title, artist, elapsed, duration):
    os.system('clear' if os.name != 'nt' else 'cls')
    spin = next(spinner)
    bar_length = 40
    progress = int((elapsed / duration) * bar_length) if duration > 0 else 0
    progress_bar = '[' + '=' * progress + ' ' * (bar_length - progress) + ']'
    color = colors[int(time.time()) % len(colors)]

    print(color + Style.BRIGHT)
    print(f"   ({spin})  {Fore.WHITE}Disco girando...  ")
    print(color + f"\n  ♫ {artist} - {title}")
    print(f"  {progress_bar} {format_time(elapsed)} / {format_time(duration)}")
    print(Fore.LIGHTBLACK_EX + "\n  Controles: [ESPAÇO]=Pausar [n]=Próxima [p]=Anterior [q]=Sair")
    print()

class MusicPlayer:
    def __init__(self):
        self.player = mpv.MPV(
            input_default_bindings=True,
            input_vo_keyboard=True,
            osc=True,
            idle=True,
            vo='null',
            quiet=True
        )
        self.current_index = 0
        self.playlist = []
        self.paused = False
        self.running = True
        self.setup_event_handlers()

    def setup_event_handlers(self):
        @self.player.event_callback('end-file')
        def end_file_handler(event):
            if event.get('reason') == 'eof':
                self.play_next()

    def list_music_files(self, folder):
        music_files = []
        for root, _, files in os.walk(folder):
            for file in files:
                if file.lower().endswith('.mp3'):
                    music_files.append(os.path.join(root, file))
        return sorted(music_files)

    def load_playlist(self, folder=None):
        folder = folder or MUSIC_FOLDER
        self.playlist = self.list_music_files(folder)
        if not self.playlist:
            print("❌ Nenhuma música encontrada em", folder)
            sys.exit()
        random.shuffle(self.playlist)
        self.save_playlist()

    def save_playlist(self):
        with open(PLAYLIST_FILE, 'w') as f:
            f.write('\n'.join(self.playlist))

    def save_to_history(self, track):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                history = f.read().splitlines()
        else:
            history = []

        if track not in history:
            with open(HISTORY_FILE, 'a') as f:
                f.write(f"{track}\n")

    def play_current(self):
        if not self.playlist:
            return
        track = self.playlist[self.current_index]
        self.player.play(track)
        self.save_to_history(track)

    def play_next(self):
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play_current()

    def play_previous(self):
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play_current()

    def toggle_pause(self):
        self.paused = not self.paused
        self.player.pause = self.paused

    def handle_controls(self):
        import termios, tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            while self.running:
                if os.read(fd, 1) == b' ':
                    self.toggle_pause()
                elif os.read(fd, 1) == b'n':
                    self.play_next()
                elif os.read(fd, 1) == b'p':
                    self.play_previous()
                elif os.read(fd, 1) == b'q':
                    self.running = False
                    break
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def run(self):
        print("🔍 Carregando músicas...")
        self.load_playlist()
        self.play_current()

        import threading
        threading.Thread(target=self.handle_controls, daemon=True).start()

        try:
            while self.running:
                metadata = self.player.metadata or {}
                title = metadata.get('title', os.path.basename(self.playlist[self.current_index]))
                artist = metadata.get('artist', 'Artista Desconhecido')
                elapsed = self.player.time_pos or 0
                duration = self.player.duration or 0
                render_disc(title, artist, elapsed, duration)
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n⏹️ Encerrando player...")
        finally:
            self.player.terminate()

def main():
    try:
        player = MusicPlayer()
        player.run()
    except ImportError:
        print("\n❌ Erro: python-mpv não está instalado")
        print("Instale com: pkg install mpv && pip install python-mpv")
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")

if __name__ == "__main__":
    main()
    
