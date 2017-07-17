# Create tables
CREATE TABLE IF NOT EXISTS User
(
    id VARCHAR(30) NOT NULL UNIQUE,
    access_token VARCHAR(250) NOT NULL,
    refresh_token VARCHAR(250) NOT NULL,
    expires_at DATETIME NOT NULL,
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
    id INT NOT NULL AUTO_INCREMENT,
    user_id VARCHAR(30) NOT NULL REFERENCES user(id),
    track_id VARCHAR(30) NOT NULL REFERENCES track(id),
    hrv LONGTEXT NOT NULL,
    date DATETIME,
    gps VARCHAR(50),
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS Recommendation
(
    id INT NOT NULL AUTO_INCREMENT,
    playlist_id VARCHAR(30) NOT NULL REFERENCES playlist(id),
    track_id VARCHAR(30) NOT NULL REFERENCES track(id),
    PRIMARY KEY(id)
);


# Create FKs
ALTER TABLE Reaction
    ADD    FOREIGN KEY (track_id)
    REFERENCES Track(id)
;
    
ALTER TABLE Reaction
    ADD    FOREIGN KEY (user_id)
    REFERENCES User(id)
;
    
ALTER TABLE Playlist
    ADD    FOREIGN KEY (user_id)
    REFERENCES User(id)
;
    
ALTER TABLE Recommendation
    ADD    FOREIGN KEY (playlist_id)
    REFERENCES Playlist(id)
;

ALTER TABLE Recommendation
    ADD    FOREIGN KEY (track_id)
    REFERENCES Track(id)
;