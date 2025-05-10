import os
import sys
import time
import mpv
from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)

MUSIC_FOLDER = "/storage/emulated/0/Music"
HISTORY_FILE = os.path.expanduser("~/.music_history")
PLAYLIST_FILE = os.path.expanduser("~/.current_playlist")

class MusicPlayer:
    def __init__(self):
        self.player = mpv.MPV(
            input_default_bindings=True,
            input_vo_keyboard=True,
            osc=False,
            idle=True,
            vo='null',
            ao='opensles',  # Força saída de áudio para Android
            quiet=True
        )
        self.current_index = 0
        self.playlist = []
        self.paused = False
        self.spinner_state = 0
        self.setup_event_handlers()
        
    def setup_event_handlers(self):
        @self.player.property_observer('time-pos')
        def time_observer(_name, value):
            if value:
                self.display_current_status()
                
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
        self.save_playlist()
        return self.playlist

    def save_playlist(self):
        with open(PLAYLIST_FILE, 'w') as f:
            f.write('\n'.join(self.playlist))

    def save_to_history(self, track):
        with open(HISTORY_FILE, 'a') as f:
            f.write(f"{track}\n")

    def spinner(self):
        spinners = ['◴', '◷', '◶', '◵']
        self.spinner_state = (self.spinner_state + 1) % 4
        return spinners[self.spinner_state]

    def display_current_status(self):
        metadata = self.player.metadata or {}
        title = metadata.get('title', os.path.basename(self.playlist[self.current_index]))
        artist = metadata.get('artist', 'Artista Desconhecido')
        duration = self.player.duration or 0
        current_pos = self.player.time_pos or 0

        def format_time(seconds):
            return time.strftime('%M:%S', time.gmtime(seconds))
        
        progress = int((current_pos / duration) * 30) if duration > 0 else 0
        bar = '=' * progress + ' ' * (30 - progress)
        disk = self.spinner()

        os.system('clear')
        print(Fore.CYAN + f"\n {disk}  {Fore.MAGENTA}{artist} - {Fore.YELLOW}{title}")
        print(Fore.GREEN + f"[{bar}] {format_time(current_pos)} / {format_time(duration)}")
        print(Style.DIM + "\n[←] Anterior  [→] Próxima  [espaço] Pausar/Retomar  [q] Sair")

    def play_current(self):
        if not self.playlist:
            return
        current_track = self.playlist[self.current_index]
        self.player.play(current_track)
        self.save_to_history(current_track)

    def play_next(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.play_current()

    def play_previous(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.play_current()

    def toggle_pause(self):
        self.paused = not self.paused
        self.player.pause = self.paused

    def run(self):
        print("🔍 Carregando músicas...")
        self.load_playlist()
        
        if not self.playlist:
            print("❌ Nenhuma música encontrada em", MUSIC_FOLDER)
            return
            
        print(f"\n🎶 {len(self.playlist)} músicas encontradas")
        self.play_current()

        try:
            while True:
                self.display_current_status()
                if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:
                    key = sys.stdin.read(1)
                    if key == 'q':
                        break
                    elif key == ' ':
                        self.toggle_pause()
                    elif key == '\x1b':  # escape sequence
                        if sys.stdin.read(1) == '[':
                            arrow = sys.stdin.read(1)
                            if arrow == 'C':
                                self.play_next()
                            elif arrow == 'D':
                                self.play_previous()
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n⏹️ Encerrando player...")
        finally:
            self.player.terminate()

import select

def main():
    player = MusicPlayer()
    player.run()

if __name__ == "__main__":
    main()
    
