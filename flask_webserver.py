from flask import Flask, request
import libs.callback_handler

app = Flask(__name__)

PORT=5000

@app.route("/callback")
def callback():
    print("A wild user appeared!")
    auth_code = request.args['code']
    #print("Code: ", auth_token)
    callback_handler.handle_new_user(auth_code)

##########################################################################################
if __name__ == "__main__":
    app.run(debug=True,port=PORT)