# heart-rate-playlist
Create Spotify playlists based on the Heart Rate reaction to music.

## Introduction
This is my graduation project for ISEL - LEIM. The idea of the project started as a way to integrate wearables and smartwatches for fisiological monitoring in a social network or networking software, such as Slack or Discord.

After the first meetings the idea faded away and started to solidify with these objectives in mind. There had to be a time where vital signs would be read and a time these signs would be used to integrate with a popular social application. We chose Spotify because it has support for development and the content it provides is appreciated by the whole world.

## SPOTIFY API
### Endpoints
* https://api.spotify.com/v1/audio-features/{id}
* https://api.spotify.com/v1/users/{user\_id}/playlists
* https://api.spotify.com/v1/users/{user\_id}/playlists
* https://api.spotify.com/v1/users/{user\_id}/playlists/{playlist\_id}/tracks
* https://api.spotify.com/v1/users/{user\_id}
* https://api.spotify.com/v1/recommendations


## Database

Currently the database holds information of each user, namely their IDs (usernames), access and refresh tokens if they authorized this app to access their personal data.

For each user multiple public playlists will be developed and I chose to hold the information of the playlist in the database as I want to depend as less as possible from Spotify. Each playlist will hold a reference for a music and some information about the playlist itself. An entity to hold the references of the music must be created as there is no type that is an array of music IDs, therefore a Playlist_Musics table will hold all the musics that are refered in playlists.

The database will also save all songs that all users heard and their audio features. This information will be relevant on the creation of playlists based not only on the user's reaction to a music but also what features the music has.

Each user will have a reaction to a music, if they are connected to the IHR reader. By having the IHR read they will send this information to a table named reaction, or context. This table will have the HRV for the music heard by the user and some other information, such as where the user heard the music (GPS) and at what time they heard the music. This is the context that the user was subject to when they heard the music.

![Database sketch](/misc/relational_database_16MAY.png "Database sketch")

## Android Client
_This project will require a means to communicate with the device that will provide the heart rate device through BLE (Bluetooth Low Energy). The way to do this is with a smartphone, we chose an Android device._

_The basic diagram showing how each component will communicate is shown below._

![Android Diagram](/misc/AndroidDiagram.png "Android Diagram")

_**THIS WON'T WORK BECAUSE THE DATA CAN'T BE RETRIEVED FROM AN APPLICATION.**_

It must be sent from the native Spotify client. I can't get the information from the Spotify client to know when a track is beginning. Other options so far:
* **Every minute** or so, query the Web API to know if the user is listening to a track (not scalable as a database with many users would render this method not viable);
* **Every minute** or so, in the Android application that will communicate with the BLE device, a request for the user's current playing track will be made, and if there is a track being played, then the heart rate should be measured.
* Another option is to completely drop the Android part of the project and use a BLE dongle to communicate with the heart rate device and get the information the hard way. This means the projects portability would be reduced to zero.

## Dependencies
For this project I decided to use Virtual Environments because it is good practice.

```
pip install virtualenv
```

The wrapper is optional but I like to use it because it makes managing virtualenvs much easier.
```
pip install virtualenvwrapper-win
```

After installing the virtualenv, you can use `workon "virtualenv-name"` to start working on this virtual environment.

#### Packages
* spotipy;
```
pip install spotipy
```
* flask;
```
pip install flask
```
* requests;
```
pip install requests
```

## Comments
Setting the redirect URI with HTTPS will cause the server to show an SSL error because of a missing certificate (from my understanding), so using only HTTP will bypass this problem.

Do not forget to log out of your Spofity account before testing with `prompt_for_user_token` or there won't be a prompt for authentication as the logged in user might already have the application authorized.

## References
* [Spotify's Web API Tutorial](https://developer.spotify.com/web-api/tutorial/)
* [Spotify's Android SDK Tutorial](https://developer.spotify.com/technologies/spotify-android-sdk/tutorial/)
* [Spotipy Documentation](https://spotipy.readthedocs.io/en/latest/)
* [Online Database Model](https://repository.genmymodel.com/tomazinhal/heart-rate-playlist)

## History

* 02-05-2017: Initial commit. 

* 04-05-2017: Started working on the README. Created prototype SQL CREATE and DROP tables files.

* 09-05-2017: Continued working on the README. Increased understanding of the Authorization FLow for the user. Started creating the connector to comunicate with the database. SQL files were updated to hold more information on the user. 

* 10-05-2017: Minimal README update.

* 11-05-2017: Started working on the database connector. Updated database model, CREATE and DROP scripts.

* 15-05-2017: Updated User table to hold the ID of each user and the datetime of expiration of the access_token. Created lib.py to be user as the main library of the application and moved methods from the login.py to this library. **Edit**: Asked some questions to professor and work colleagues and finally figured out how the Authentication worked. Now to get the server to correctly manage the requests will be another issue. Also updated README.

* 16-05-2017: Renamed MUSIC table to TRACK and started began working on relevant track information. Updated Database information with most recent model.

* 18-05-2017: Massive refactor. Created `/libs` and `/testing` to hold the main code to be used as libraries and tests to be made to make sure everything keeps working. 

* 20-05-2017: Create playlist method. Updated testing to create playlist.

* 21-05-2017: Add track method. Incomplete.

* 22-05-2017: Continued track method. Started working on Android client. *** Edit ***: This won't work because you can't get information from an application in Android, it must be willingly sent by the application.

* 23-05-2017: Massive roadblock encountered. Need instructions and help. See #Android Client.