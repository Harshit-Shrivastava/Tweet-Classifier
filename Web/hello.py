from flask import Flask
from BusinessLayer.getTweets import flaskPOC

app = Flask(__name__)

@app.route("/")
def hello():
    return flaskPOC()

if __name__ == "__main__":
    app.run()