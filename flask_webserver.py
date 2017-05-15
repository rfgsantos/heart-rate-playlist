import json
from flask import Flask, request, redirect, g, render_template
import requests
import base64
import urllib

import lib

app = Flask(__name__)

PORT=5000

#  Client Keys
CREDENTIALS_FILE = "configs/credentials.json"
creds = lib.get_spotify_credentials(CREDENTIALS_FILE)
CLIENT_ID = creds['SPOTIFY_APP_ID']
CLIENT_SECRET = creds['SPOTIFY_APP_SECRET']
REDIRECT_URI = creds['SPOTIFY_REDIRECT_URI']

# Spotify URLS
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

@app.route("/callback")
def callback():
    print("Service requested!")
    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    print("Code: ", auth_token)
    code_payload = {
        "grant_type": "authorization_code",
        "code": auth_token,
        "redirect_uri": REDIRECT_URI
    }
    base64encoded = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET).encode("ascii"))
    print("Encoded: ", base64encoded)
    headers = {"Authorization": "Basic {}".format(base64encoded)}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    print(response_data)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]


##########################################################################################
if __name__ == "__main__":
    app.run(debug=True,port=PORT)