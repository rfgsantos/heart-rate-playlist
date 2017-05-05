# Create tables
CREATE TABLE IF NOT EXISTS User
(
    id VARCHAR(15) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS Playlist
(
    id VARCHAR(15) NOT NULL,
    user_id VARCHAR(15),
    comment VARCHAR(250),
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS Music
(
    id VARCHAR(15) NOT NULL,
    playlist VARCHAR(15),
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS Reaction
(
    hrv LONGTEXT NOT NULL,
    user_id VARCHAR(15),
    music_id VARCHAR(15),
    date TIME,
    gps DOUBLE,
    pr_id INT,
    PRIMARY KEY(hrv)
);

# Create FKs
ALTER TABLE Music
    ADD    FOREIGN KEY (playlist)
    REFERENCES Playlist(id)
;
    
ALTER TABLE Reaction
    ADD    FOREIGN KEY (music_id)
    REFERENCES Music(id)
;
    
ALTER TABLE Playlist
    ADD    FOREIGN KEY (user_id)
    REFERENCES User(id)
;
    
ALTER TABLE Reaction
    ADD    FOREIGN KEY (user_id)
    REFERENCES User(id)
;