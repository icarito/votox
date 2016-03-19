from flask import Flask
from flask import request
from flask import g

import shelve
import json

from os import path
from cPickle import HIGHEST_PROTOCOL
from contextlib import closing

SHELVE_DB = 'shelve.db'

app = Flask(__name__)
app.config.from_object(__name__)

db = shelve.open(path.join(app.root_path, app.config['SHELVE_DB']),
                 protocol=HIGHEST_PROTOCOL, writeback=True)

@app.route("/vote", methods=["POST"])
def hello():
    uniq = str(request.form['uniq'])
    opcion = request.form['opcion']
    if not uniq in db:
        db[uniq] = opcion
        return "Su voto ha sido guardado."
    else:
        return "No puede votar dos veces."

@app.route("/dump", methods=["GET"])
def dump():
    return json.dumps(dict(db))

if __name__ == "__main__":
    with closing(db):
        app.run()
