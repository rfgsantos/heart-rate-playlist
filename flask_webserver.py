import sys
sys.path.append("libs/")
import callback_handler

from flask import Flask, request

app = Flask(__name__)

PORT=5000

@app.route("/new_user")
def new_user():
    print("A wild user appeared!")
    auth_code = request.args['code']
    #print("Code: ", auth_token)
    callback_handler.handle_new_user(auth_code)
    print("User caught!")

@app.route("/new_reaction")
def new_reaction():
    print("A user felt something!")
    #get user's reaction
    information = "user_id, music_id, heart-rate-stuff, gps, time"
    callback_handler.handle_new_reaction(information)
    print("Reaction handled!")

##########################################################################################
if __name__ == "__main__":
    app.run(debug=True,port=PORT)