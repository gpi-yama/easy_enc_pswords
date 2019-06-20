from flask import Flask, render_template, request
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import base64
import hashlib

salt = b'\x04\xa8y#AN\xba\xb0u\x0c\xd2\xbd"\x002p'
iv = b"hoge"
raw = b"51235"
raw2 = b"tasegd"
raw3 = b"gasdgf"
psword = b"turbulentcontrol"
#print(raw)
raw = base64.b64encode(raw)

if len(raw) % 16 != 0:
    for i in range(16 - len(raw) % 16):
        raw += b'_'

if len(raw2) % 16 != 0:
    for i in range(16 - len(raw2) % 16):
        raw2 += b'_'

if len(raw3) % 16 != 0:
    for i in range(16 - len(raw3) % 16):
        raw3 += b'_'

print(raw3)
h = SHA256.new()
h.update(bytes(psword))
key = h.digest()
iv = hashlib.md5(iv).digest()
cipher = AES.new(key, AES.MODE_CBC, iv)
ctxt = cipher.encrypt(raw)
ctxt2 = cipher.encrypt(raw2)
ctxt3 = cipher.encrypt(raw3)
#ctxt = base64.b64encode(ctxt)

#print(ctxt3)

#plain = base64.b64decode(ctxt)

cipher = AES.new(key, AES.MODE_CBC, iv)

plain = cipher.decrypt(ctxt)
plain2 = cipher.decrypt(ctxt2)
plain3 = cipher.decrypt(ctxt3)

print(plain3)
print(base64.b64decode(plain3))
