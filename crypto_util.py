from flask import Flask, render_template, request, redirect
from Crypto.Cipher import AES
from Crypto.Hash import SHA256, MD5
import sqlite3
import base64
from constants import *
from Crypto import Random

def get_iv(ctxt):
    ctxt = base64.b64decode(ctxt)
    iv = ctxt[:16]
    ctxt = ctxt[16:]
    return base64.b64encode(ctxt), base64.b64encode(iv) 

class SimpleCrypto:
    def __init__(self):
        self.__iv = Random.new().read(AES.block_size)
        self.__salt = salt
        
    def _pad(self, txt):
        return txt + (BS - len(txt) % BS) * chr(BS - len(txt) % BS)

    def _unpad(self, txt):
        return txt[:-ord(txt[len(txt)-1:])]
    
    def encrypt(self, ptxt: list, psword: str):
        md5 = MD5.new()
        h = SHA256.new()

        # streaching
        for i in range(1000):
            if i == 0:
                key = bytes(psword, encoding="utf8") + self.__salt
            else:
                key += bytes(psword, encoding="utf8") + self.__salt
            h.update(key)
            key = h.digest()

        cipher = AES.new(key, AES.MODE_CBC, self.__iv)
        
        ctxt = []
        i = 0
        for txt in ptxt:
            c = cipher.encrypt(self._pad(txt))
            if i == 0:
                c = self.__iv + c
                i = 1
            c = base64.b64encode(c)
            ctxt.append(c)

        del key
        return ctxt

    def decrypt(self, ctxt: list, psword: str, iv=None):
        if iv is not None:
            self.__iv = base64.b64decode(iv)
        h = SHA256.new()

        # streaching
        for i in range(1000):
            if i == 0:
                key = bytes(psword, encoding="utf8") + self.__salt
            else:
                key += bytes(psword, encoding="utf8") + self.__salt
            h.update(key)
            key = h.digest()

        ctxt = [base64.b64decode(t) for t in ctxt]
        self.__iv, ctxt[0] = ctxt[0][:16], ctxt[0][16:]
        cipher = AES.new(key, AES.MODE_CBC, self.__iv)
        
        ptxt = []
        i == 0
        for t in ctxt:
            ctxt = cipher.decrypt(t)
            ptxt.append(self._unpad(ctxt))

        del key
        return ptxt

if __name__ == "__main__":
    scheme = SimpleCrypto()
    ctxt, iv = scheme.encrypt(["OK", "BAD", "NG"], "TEST")
    print(ctxt)
    ptxt = scheme.decrypt(ctxt, "TEST", iv)
    print(ptxt)
    print(AES.block_size)