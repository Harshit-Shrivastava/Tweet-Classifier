from flask import Flask, render_template
from BusinessLayer.getTweets import flaskPOC
from BusinessLayer.getTweets import pullTweets

app = Flask(__name__)

@app.route("/")
def static_page():
    return render_template('index.html')

@app.route("/pullTweets")
def getData():
    pullTweets()
    return "Training data created"

if __name__ == "__main__":
    app.run()