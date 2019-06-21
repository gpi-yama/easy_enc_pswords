from flask import Flask, render_template, request, redirect
from Crypto.Cipher import AES
from Crypto.Hash import SHA256, MD5
import sqlite3
import base64

app = Flask(__name__)

db_name = "cryptodb"

iv_base = b"qrpgg02934g"
salt = b'\x04\xa8y#AN\xba\xb0u\x0c\xd2\xbd"\x002p'
user = None


def authorization(user, psword):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    try:
        psdb = c.execute(
            "SELECT psword IN users WHERE user = " + str(user))
        h = SHA256.new()
        h.update(bytes(psword) + salt)
        key = h.digest()
        if str(key) == psword:
            return True
    except:
        return False


def pad(txt):
    if len(txt) % 16 != 0:
        for i in range(16 - len(txt) % 16):
            txt += b'_'
    return txt


def unpad(txt):
    un_txt = ""
    n = 0
    for t in txt[::-1]:
        if t != "_":
            un_txt = txt[:len(txt) - n]
            return un_txt
        n += 1


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

    psword = bytes(psword, encoding="utf8")
    h = SHA256.new()
    h.update(bytes(psword)+salt)
    psword = h.hexdigest()

    db = sqlite3.connect(db_name)
    c = db.cursor()
    print("SELECT ID FROM users WHERE user = " + user)
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

        psword = bytes(psword, encoding="utf8")
        server = bytes(server, encoding="utf8")
        pc = bytes(pc, encoding="utf8")
        other = bytes(other, encoding="utf8")
        key = bytes(key, encoding="utf8") + salt

        raw = [server, pc, other]

        raw = [pad(t) for t in raw]

        h = SHA256.new()
        h.update(bytes(psword)+salt)
        psword = h.hexdigest()

        autho = authorization(user, psword)

        if autho is False:
            redirect("/")

        md5 = MD5.new()
        md5.update(iv_base)
        iv = md5.digest()
        print(iv)
        h.update(key)
        key = h.digest()

        cipher = AES.new(key, AES.MODE_CBC, iv)
        ctxt = []
        for txt in raw:
            c = cipher.encrypt(txt)
            c = base64.b64encode(c)
            ctxt.append(c)

        db = sqlite3.connect(db_name)
        c = db.cursor()
        print('INSERT INTO ctxt VALUES (NULL, "{0}", "{1[0]}", "{1[1]}", "{1[2]}")'.format(
            user, list(map(lambda x: str(x), ctxt))))
        
        c.execute('INSERT INTO ctxt VALUES (NULL, "{0}", "{1[0]}", "{1[1]}", "{1[2]}")'.format(
            user, list(map(lambda x: str(x), ctxt))))
        
        db.commit()
        db.close()
        ctxt = list(map(lambda x: str(x), ctxt))
        del key, iv, cipher, h, md5
        return render_template("crypto.html", user=user, server=ctxt[0], pc=ctxt[1], other=ctxt[2])
        del ctxt

    else:
        redirect("/")


@app.route('/decrypt', methods=["GET", "POST"])
def decrypt():
    if request.method == "POST":
        user = request.form["user"]
        psword = request.form["password"]
        key = request.form["key"]

    psword = bytes(psword, encoding="utf8")
    autho = authorization(user, psword)
    if autho is False:
        redirect("/")

    key = bytes(key, encoding="utf8") + salt

    md5 = MD5.new()
    md5.update(iv_base)
    iv = md5.digest()
    h = SHA256.new()
    h.update(key)
    key = h.digest()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    raw = []

    db = sqlite3.connect(db_name)
    c = db.cursor()
    ct = c.execute("SELECT * FROM ctxt WHERE user = '{0}';".format(user))
    for cs in ct:
        ctxts = list(cs)[2:]

    for ctxt in ctxts:
        ct = ctxt[2:-1]
        raw.append(cipher.decrypt(base64.b64decode(ct)))
    print(raw)
    raw = list(map(lambda x: unpad(x.decode("utf-8")), raw))

    del key, iv, cipher, h, md5
    return render_template("decrypt.html", user=user, server=raw[0], pc=raw[1], other=raw[2])
    del ctxt


if __name__ == "__main__":
    app.run(debug=True, port=8888)
