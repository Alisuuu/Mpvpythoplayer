import os
import sys
import time
import mpv
from pathlib import Path

# Configurações
MUSIC_FOLDER = "/storage/emulated/0/Music"
HISTORY_FILE = os.path.expanduser("~/.music_history")
PLAYLIST_FILE = os.path.expanduser("~/.current_playlist")

class MusicPlayer:
    def __init__(self):
        self.player = mpv.MPV(
            input_default_bindings=True,
            input_vo_keyboard=True,
            osc=True,
            idle=True,
            vo='null',  # Modo sem vídeo
            quiet=True
        )
        self.current_index = 0
        self.playlist = []
        self.paused = False
        self.setup_event_handlers()
        
    def setup_event_handlers(self):
        @self.player.property_observer('time-pos')
        def time_observer(_name, value):
            if value:
                self.display_current_status()
                
        @self.player.event_callback('end-file')
        def end_file_handler(event):
            if event['reason'] == 'eof':
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

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                return f.read().splitlines()
        return []

    def save_to_history(self, track):
        history = self.load_history()
        if track not in history:
            with open(HISTORY_FILE, 'a') as f:
                f.write(f"{track}\n")

    def display_current_status(self):
        metadata = self.player.metadata or {}
        title = metadata.get('title', os.path.basename(self.playlist[self.current_index]))
        artist = metadata.get('artist', 'Artista Desconhecido')
        duration = self.player.duration or 0
        current_pos = self.player.time_pos or 0
        
        # Barra de progresso
        progress = int((current_pos / duration) * 50) if duration > 0 else 0
        progress_bar = '[' + '=' * progress + ' ' * (50 - progress) + ']'
        
        # Tempo formatado
        def format_time(seconds):
            return time.strftime('%M:%S', time.gmtime(seconds))
        
        print(f"\n🎵 {artist} - {title}")
        print(f"{progress_bar} {format_time(current_pos)} / {format_time(duration)}")
        print(f"\nControles: ⏯️ Espaço = Pausar | ⏭️ → = Próxima | ⏮️ ← = Anterior | ⏹️ q = Sair")

    def play_current(self):
        if not self.playlist:
            return
            
        current_track = self.playlist[self.current_index]
        self.player.play(current_track)
        self.save_to_history(current_track)
        self.display_current_status()

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
        print("⏸️ Pausado" if self.paused else "▶️ Retomando")

    def shuffle_playlist(self):
        import random
        random.shuffle(self.playlist)
        self.current_index = 0
        self.save_playlist()
        print("\n🔀 Playlist embaralhada!")

    def show_playlist(self):
        print("\n🎵 Playlist Atual:")
        for i, track in enumerate(self.playlist):
            prefix = "▶ " if i == self.current_index else "  "
            print(f"{prefix}{i+1}. {os.path.basename(track)}")

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
                # O MPV lida com os controles de teclado automaticamente
                # Manter o processo rodando
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⏹️ Encerrando player...")
        finally:
            self.player.terminate()

def main():
    # Verifica se o mpv está instalado
    try:
        player = MusicPlayer()
        player.run()
    except ImportError:
        print("\n❌ Erro: python-mpv não está instalado")
        print("Instale com:")
        print("1. pkg install mpv")
        print("2. pip install python-mpv")
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")

if __name__ == "__main__":
    main()