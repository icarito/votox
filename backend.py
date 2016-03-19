from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/vote", methods=["POST"])
def hello():
    print request.form['uniq']
    print request.form['opcion']
    return "OK"

if __name__ == "__main__":
    app.run()
