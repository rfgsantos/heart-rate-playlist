# Create database
CREATE DATABASE IF NOT EXISTS hear_rate_spotify;

# Create tables
CREATE TABLE IF NOT EXISTS User
(
    id VARCHAR(50) NOT NULL,
    refresh_token VARCHAR(250) NOT NULL,
    access_token VARCHAR(250) NOT NULL,
    lifespan INT NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS Playlist
(
    id VARCHAR(50) NOT NULL,
    user_id VARCHAR(50),
    comment VARCHAR(250),
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS Music
(
    id VARCHAR(50) NOT NULL,
    playlist VARCHAR(50),
    comment VARCHAR(250),
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS Recommended
(
    id INT NOT NULL AUTO_INCREMENT,
    playlist_id VARCHAR(50),
    music_id VARCHAR(50),
    PRIMARY KEY(id)
)

CREATE TABLE IF NOT EXISTS Reaction
(
    id INT NOT NULL AUTO_INCREMENT,
    hrv MEDIUMTEXT NOT NULL,
    user_id VARCHAR(50),
    music_id VARCHAR(50),
    date TIME,
    gps DOUBLE,
    PRIMARY KEY(id)
);

# Create FKs
ALTER TABLE Music
    ADD    FOREIGN KEY (playlist)
    REFERENCES Playlist(id)
;
    
ALTER TABLE Playlist
    ADD    FOREIGN KEY (user_id)
    REFERENCES User(id)
;
        
ALTER TABLE Reaction
    ADD    FOREIGN KEY (music_id)
    REFERENCES Music(id)
;

ALTER TABLE Reaction
    ADD    FOREIGN KEY (user_id)
    REFERENCES User(id)
;

ALTER TABLE Recommended
    ADD FOREIGN KEY (playlist_id)
    REFERENCES Playlist(id)
;

ALTER TABLE Recommended
    ADD FOREIGN KEY (music_id)
    REFERENCES Musid(id)
;