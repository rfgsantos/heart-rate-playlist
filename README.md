# heart-rate-playlist
Create Spotify playlists based on the Heart Rate reaction to music.

## Introduction
This is my graduation project for ISEL - LEIM. The idea of the project started as a way to integrate wearables and smartwatches for fisiological monitoring in a social network or networking software, such as Slack or Discord.

After the first meetings the idea faded away and started to solidify with these objectives in mind. There had to be a time where vital signs would be read and a time these signs would be used to integrate with a popular social application. We chose Spotify because it has support for development and the content it provides is appreciated by the whole world.

## Database

Currently the database holds information of each user, namely their IDs (usernames), access and refresh tokens if they authorized this app to access their personal data.

For each user multiple public playlists will be developed and I chose to hold the information of the playlist in the database as I want to depend as less as possible from Spotify. Each playlist will hold a reference for a music and some information about the playlist itself. An entity to hold the references of the music must be created as there is no type that is an array of music IDs, therefore a Playlist_Musics table will hold all the musics that are refered in playlists.

The database will also save all songs that all users heard and their audio features. This information will be relevant on the creation of playlists based not only on the user's reaction to a music but also what features the music has.

Each user will have a reaction to a music, if they are connected to the IHR reader. By having the IHR read they will send this information to a table named reaction, or context. This table will have the HRV for the music heard by the user and some other information, such as where the user heard the music (GPS) and at what time they heard the music. This is the context that the user was subject to when they heard the music.


## Dependencies
For this project I decided to use Virtual Environments because it is good practice.

TODO: Instructions to install venv and virtualenvwrapper.

After installing the virtualenv, these are the packages required for this project:
TODO: List packages.
 * spotipy;
 * flask;
 * requests (which should be fulfilled when installing spotipy);


## History

02-05-2017: Initial commit. 

04-05-2017: Started working on the README. Created prototype SQL CREATE and DROP tables files.

09-05-2017: Continued working on the README. Increased understanding of the Authorization FLow for the user. Started creating the connector to comunicate with the database. SQL files were updated to hold more information on the user. 

10-05-2017: Minimal README update.

11-05-2017: Started working on the database connector. Updated database model, CREATE and DROP scripts.

15-05-2017: Updated User table to hold the ID of each user and the datetime of expiration of the access_token. Created lib.py to be user as the main library of the application and moved methods from the login.py to this library.