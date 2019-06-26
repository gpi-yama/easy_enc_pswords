from flask import Flask, render_template, request, redirect
from Crypto.Hash import SHA256, MD5
import sqlite3

from constants import *
from crypto_util import SimpleCrypto, get_iv
from autho import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("menu.html")


@app.route("/signup")
def sign():
    return render_template("sign.html")


@app.route("/dec_menu")
def dec_menu():
    return render_template("dec_menu.html")


@app.route('/signup/sign', methods=["GET", "POST"])
def signup():
    user = request.form["user"]
    psword = request.form["password"]

    psword = mkpsword(psword)

    db = sqlite3.connect(db_name)
    c = db.cursor()
    try:
        psdb = c.execute("SELECT ID FROM users WHERE user = " + user)
    except:
        c.execute(
            "INSERT INTO users VALUES (NULL, '{0}', '{1}')".format(str(user), str(psword)))
        db.commit()
    db.close()

    return render_template("menu.html")


@app.route('/encrypt', methods=["GET", "POST"])
def encrypt():
    if request.method == "POST":
        user = request.form["user"]
        psword = request.form["password"]
        key = request.form["key"]
        server = request.form["server"]
        pc = request.form["pc"]
        other = request.form["other"]

        raw = [server, pc, other]

        psword = mkpsword(psword)
        print(psword)
        autho = authorization(user, psword)
        print("autho", autho)
        if autho is False:
            return redirect("/")

        scheme = SimpleCrypto()
        ctxt = scheme.encrypt(raw, key)
        
        db = sqlite3.connect(db_name)
        c = db.cursor()
        ct = None
        que = c.execute("SELECT * FROM ctxt WHERE user = '{0}';".format(user))
        
        for t in que:
            ct = t

        if ct is not None:
            print("update!")
            c.execute('UPDATE ctxt SET server="{0[0]}", pc="{0[1]}", other="{0[2]}" WHERE user = "{1}"'.format(ctxt, user))
        else:
            print("insert!")
            c.execute('INSERT INTO ctxt VALUES (NULL, "{0}", "{1[0]}", "{1[1]}", "{1[2]}")'.format(
                user, ctxt))
        
        db.commit()
        db.close()
        
        ctxt = list(map(lambda x: str(x), ctxt))
        del key
        return render_template("crypto.html", user=user, server=ctxt[0], pc=ctxt[1], other=ctxt[2])

    else:
        return redirect("/")


@app.route('/decrypt', methods=["GET", "POST"])
def decrypt():
    if request.method == "POST":
        user = request.form["user"]
        psword = request.form["password"]
        key = request.form["key"]

    psword = mkpsword(psword)
    autho = authorization(user, psword)
    if autho is False:
        return redirect("/")

    db = sqlite3.connect(db_name)
    c = db.cursor()
    ct = c.execute("SELECT * FROM ctxt WHERE user = '{0}';".format(user))

    for cs in ct:
        ctxt = list(cs)[2:]

    for i in range(len(ctxt)):
        ctxt[i] = ctxt[i][2:-1]

    scheme = SimpleCrypto()
    raw = scheme.decrypt(ctxt, key)

    del key
    return render_template("decrypt.html", user=user, server=raw[0].decode(), pc=raw[1].decode(), other=raw[2].decode())

if __name__ == "__main__":
    app.run(debug=True, port=8888)
