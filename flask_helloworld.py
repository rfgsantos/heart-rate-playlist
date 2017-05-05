from flask_oauthlib.client import OAuth, OAuthException
from flask import Flask, jsonify, abort, make_response, redirect, url_for, session, request
import requests as req

OAUTH_OKEN = "BQBZ_rpCDzkahYalrjeO_L1gXjztJyFrMsidAvDb5dl2HjLq4nqqmV-4kLhvAMKvMpL7sex0QmEfO8nnryyXAqDOsK25PTbHuuJLqTbdCFlkp--Rvjd6LH7qGHgeeojkXKRoEyh3c6Ao-DdqChwzlD4FQ2OuERCGbRdV"
tomazinhal_url = "https://api.spotify.com/v1/users/11122241033"

SPOTIFY_APP_ID = '9efc6cfd070049e18043aee96ae5228a'
SPOTIFY_APP_SECRET = 'b6eea41f283446c78b0dbee02e3df4b7'
SPOTIFY_REDIRECT_URI = 'https://localhost:5000/callback'

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

spotify = oauth.remote_app(
    'spotify',
    consumer_key=SPOTIFY_APP_ID,
    consumer_secret=SPOTIFY_APP_SECRET,
    # Change the scope to match whatever it us you need
    # list of scopes can be found in the url below
    # https://developer.spotify.com/web-api/using-scopes/
    request_token_params={'scope': 'user-read-email'},
    base_url='https://accounts.spotify.com',
    request_token_url=None,
    access_token_url='/api/token',
    authorize_url='https://accounts.spotify.com/authorize'
)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login')
def login():
    callback = url_for(
        'spotify_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True
    )
    return spotify.authorize(callback=callback)


@app.route('/login/authorized')
def spotify_authorized():
    resp = spotify.authorized_response()
    if resp is None:
        return 'Access denied: reason={0} error={1}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    if isinstance(resp, OAuthException):
        return 'Access denied: {0}'.format(resp.message)

    session['oauth_token'] = (resp['access_token'], '')
    me = spotify.get('/me')
    return 'Logged in as id={0} name={1} redirect={2}'.format(
        me.data['id'],
        me.data['name'],
        request.args.get('next')
    )


@spotify.tokengetter
def get_spotify_oauth_token():
    return session.get('oauth_token')


##########################################################################################
if __name__ == "__main__":
    app.run()