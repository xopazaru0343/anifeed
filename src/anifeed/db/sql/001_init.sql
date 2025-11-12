CREATE TABLE IF NOT EXISTS anime(
        anime_id INTEGER NOT NULL,
        source TEXT  NOT NULL,
        title_romaji TEXT  NOT NULL, 
        title_english TEXT  NOT NULL, 
        status TEXT NOT NULL, 
        episodes INTEGER,
        PRIMARY KEY(anime_id, source)
        );
CREATE TABLE IF NOT EXISTS torrent(
        torrent_sk INTEGER PRIMARY KEY AUTOINCREMENT,
        torrent_id INTEGER NOT NULL,
        title TEXT NOT NULL, 
        download_url TEXT NOT NULL, 
        size TEXT, 
        seeders INTEGER, 
        leechers INTEGER,
        anime_id INTEGER NOT NULL,
        anime_source TEXT NOT NULL,
        UNIQUE (torrent_sk, torrent_id)
        FOREIGN KEY(anime_id, anime_source) REFERENCES anime(anime_id, source)
        );