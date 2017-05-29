from flask import Flask, request
import libs.callback_handler

app = Flask(__name__)

PORT=5000

@app.route("/new_user")
def new_user():
    print("A wild user appeared!")
    auth_code = request.args['code']
    #print("Code: ", auth_token)
    callback_handler.handle_new_user(auth_code)
    print("User caught!")

@app.route("/new_reaction", methods=['POST'])
def new_reaction():
    print("A user felt something!")
    reaction = {
        'user_id': request.get('user_id'),
        'track_id': request.get('track_id'),
        'location': request.get('location'),
        'datetime': request.get('datetime'),
        'heart_rate': request.get('heart_rate')
    }
    callback_handler.handle_new_reaction(reaction)
    print("Reaction handled!")

##########################################################################################
if __name__ == "__main__":
    app.run(debug=True,port=PORT)