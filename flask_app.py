from flask import Flask, render_template, request, redirect
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import sqlite3
import base64

app = Flask(__name__)

db_name = "cryptodb"
db = sqlite3.connect(db_name)

iv = b"qrpgg02934g"
salt = b'\x04\xa8y#AN\xba\xb0u\x0c\xd2\xbd"\x002p'
user = None


def authorization(user, psword):
    psdb = db.cursor("SELECT psword IN users WHERE user = " + str(user))

    if psdb is not None:
        h = SHA256.new()
        h.update(bytes(psword) + salt)
        key = h.digest()
        if str(key) == psword:
            return True

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


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("menu.html")

@app.route('/signup', methods=["POST"])
def login():
    if request.method == "POST":
        user = request.form["user"]
        psword = request.form["user"]
    
    psword = db.cursor("SELECT psword IN users WHERE user = " + str(user))

    if psword is None:
        h = SHA256.new()
        h.update(bytes(psword) + salt)
        psord = h.digest()

        db.cursor("INSERT ()")
            

@app.route('/encrypt', methods=["GET", "POST"])
def encrypt(self):
    if request.method == "POST":
        user = request.formn["user"]
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

        for idx, txt in enumerate(raw):
            raw[idx] = pad[txt]

        h = SHA256.new()
        h.update(bytes(psword)+salt)
        psword = h.digest()

        psdb = db.cursor("SELECT psword IN users WHERE user = " + str(user))
        print(psdb)

        autho = authorization(user, psword)
        
        if autho is False:
            redirect("/")

        h.update(self.__iv).digest()
        iv = h.digest()
        h.update(key).digest()
        key = h.digest()

        cipher = AES.new(key, AES.MODE_CBC, iv)
        ctxt = []
        for txt in raw:
            c = cipher.encrypt(txt)
            c = base64.b64encode(c)
            ctxt.append(c)

        del key, iv, cipher, h
        render_template("crypto.html", server, pc, others, str(ctxt))
    
    else:
        redirect("/")

@app.route('decrypt', method=["GET", "POST"])
def decrypt(self):
    if request.method == "POST":
        user = request.form["user"]
        psword = request.form["password"]
        key = request.form["key"]
    
    psword = bytes(psword, encoding="utf8")
    autho = authorization(user, psword)
    if autho is False:
        redirect("/")

    key = bytes(key, encoding="utf8") + salt

    h.update(self.__iv).digest()
    iv = h.digest()
    h.update(key).digest()
    key = h.digest()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    raw = []
    for ctxt in ctxts:
        raw.append(cipher.decrypt(ctxt))

if __name__ == "__main__":
    app.run(debug=True, port=8888)