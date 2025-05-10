const fs = require('fs');
const path = require('path');
const Aplay = require('node-aplay');

// Configurações
const MUSIC_FOLDER = '/storage/emulated/0/Music';  // Caminho para a pasta de músicas
let playlist = [];

// Função para listar arquivos .mp3
function listMusicFiles(folder) {
    let musicFiles = [];
    function readFolder(currentFolder) {
        const files = fs.readdirSync(currentFolder);
        files.forEach(file => {
            const filePath = path.join(currentFolder, file);
            const stat = fs.statSync(filePath);

            if (stat.isDirectory()) {
                readFolder(filePath);  // Recursivamente buscar em subpastas
            } else if (file.toLowerCase().endsWith('.mp3')) {
                musicFiles.push(filePath);
            }
        });
    }
    readFolder(folder);
    return musicFiles;
}

// Função para tocar a música
function playMusic(filePath) {
    console.log(`Tocando: ${filePath}`);
    const player = new Aplay(filePath);
    player.play();

    player.on('complete', () => {
        playNext(); // Toca a próxima música automaticamente após terminar
    });
}

// Função para tocar a próxima música
function playNext() {
    if (playlist.length === 0) {
        console.log('Sem músicas na playlist!');
        return;
    }

    const currentSong = playlist.shift();  // Remove a música atual da playlist
    playMusic(currentSong);  // Toca a próxima música
}

// Função para carregar e exibir a playlist
function loadPlaylist() {
    playlist = listMusicFiles(MUSIC_FOLDER);
    console.log('Playlist carregada:');
    playlist.forEach((song, index) => {
        console.log(`${index + 1}: ${song}`);
    });

    playNext(); // Inicia a reprodução com a primeira música
}

// Inicia o player
function main() {
    console.log('Carregando músicas...');
    loadPlaylist();
}

// Executar o player
main();
