# Create tables
CREATE TABLE IF NOT EXISTS User
(
    id VARCHAR(30) NOT NULL UNIQUE,
    access_token VARCHAR(250) NOT NULL,
    refresh_token VARCHAR(250) NOT NULL,
    expires_at DATE NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS Playlist
(
    id VARCHAR(30) NOT NULL UNIQUE,
    user_id VARCHAR(30) NOT NULL,
    comment VARCHAR(250),
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS Track
(
    id VARCHAR(30) NOT NULL UNIQUE,
    duration_sec DECIMAL(6, 3) NOT NULL,
    danceability DECIMAL(4, 3) NOT NULL,
    energy DECIMAL(4, 3) NOT NULL,
    loudness DECIMAL(5, 3) NOT NULL,
    track_key SMALLINT NOT NULL,
    liveness DECIMAL(4, 3) NOT NULL,
    valence DECIMAL(4, 3) NOT NULL,
    tempo DECIMAL(6, 3) NOT NULL,
    time_signature SMALLINT NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS Reaction
(
    user_id VARCHAR(30) NOT NULL,
    track_id VARCHAR(30) NOT NULL,
    hrv LONGTEXT NOT NULL,
    date TIME,
    gps DOUBLE    
);

CREATE TABLE IF NOT EXISTS Recommended
(
    id INT NOT NULL UNIQUE,
    track_id VARCHAR(30) NOT NULL,
    playlist_id VARCHAR(30) NOT NULL,
    PRIMARY KEY(id)
);


# Create FKs
ALTER TABLE Reaction
    ADD    FOREIGN KEY (track_id)
    REFERENCES Track(id)
;
    
ALTER TABLE Playlist
    ADD    FOREIGN KEY (user_id)
    REFERENCES User(id)
;
    
ALTER TABLE Reaction
    ADD    FOREIGN KEY (user_id)
    REFERENCES User(id)
;
    
ALTER TABLE Recommended
    ADD    FOREIGN KEY (track_id)
    REFERENCES Track(id)
;
    
ALTER TABLE Recommended
    ADD    FOREIGN KEY (playlist_id)
    REFERENCES Playlist(id)
;