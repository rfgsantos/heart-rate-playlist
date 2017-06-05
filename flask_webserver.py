import sys
sys.path.append("libs/")
import callback_handler

from flask import Flask, request

app = Flask(__name__)

PORT=5000

@app.route("/")
def index():
    return "This is the homepage"

@app.route("/new_user")
def new_user():
    print("A wild user appeared!")
    auth_code = request.args['code']
    #print("Code: ", auth_token)
    callback_handler.handle_new_user(auth_code)
    print("User caught!")
    return("USER CAUGHT!")

@app.route("/new_reaction", methods=['POST'])
def new_reaction():
    print("A user felt something!")
    reaction = {
        'user_id': request.form['user_id'],
        'track_id': request.form['track_id'],
        'location': request.form['location'],
        'datetime': request.form['datetime'],
        'heart_rate': request.form['heart_rate']
    }
    callback_handler.handle_new_reaction(reaction)
    print("Reaction handled!")
    return("REACTION CAPTURED!")

##########################################################################################
if __name__ == "__main__":
    app.run(debug=True,port=PORT)