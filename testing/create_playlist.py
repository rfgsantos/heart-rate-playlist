import spotipy
import login
import connector

if __name__ == "__main__":
    #authorizing app to use a user's information
    soa = spotipy.oauth2.SpotifyOAuth(client_id=login.SPOTIFY_APP_ID, client_secret=login.SPOTIFY_APP_SECRET, redirect_uri=login.SPOTIFY_REDIRECT_URI, scope=login.SPOTIFY_SCOPE)
    refresh_token, lifespan, access_token = login.get_cached_token("tomaz.spotify")
    response = soa.refresh_access_token(refresh_token)
    print(response)
    new_token = response['access_token']
    sp = spotipy.Spotify(auth=new_token)
    
    #getting playlists
    playlists = sp.current_user_playlists()
    playlist_names = [p['name'] for p in playlists['items']]
    print(playlist_names)

    #creating playlist
    id = sp.me()['id']# user id is required
    resp = sp.user_playlist_create(id, "TESTEST")

    #proving it works
    playlists = sp.current_user_playlists()
    playlist_names = [p['name'] for p in playlists['items']]
    print(playlist_names)
