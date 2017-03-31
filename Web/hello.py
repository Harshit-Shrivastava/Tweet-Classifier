from flask import Flask, render_template
from BusinessLayer.getTweets import flaskPOC

app = Flask(__name__)

@app.route("/")
def static_page():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()