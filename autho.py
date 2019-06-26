from Crypto.Hash import SHA256, MD5
from constants import *
import sqlite3

def mkpsword(psword):
    psword = bytes(psword, encoding="utf8")
    h = SHA256.new()
    for i in range(1000):
        if i == 0:
            psword_hash = bytes(psword)+salt
        else:
            psword_hash += bytes(psword)+salt
        h.update(psword_hash)
        psword_hash = h.digest()
    psword_hash = h.hexdigest()
    
    return psword_hash


def authorization(user, psword):
    db = sqlite3.connect(db_name)
    c = db.cursor()
    #try:
    psdb = c.execute(
        'SELECT * from users WHERE user = "{0}"'.format(user))
    for t in psdb:
        psword_db = t[2]
    
    if psword_db == psword:
        print("FASFSAFSFASF!!!")
        return True
    #except:
        #return False