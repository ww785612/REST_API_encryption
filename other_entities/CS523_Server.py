#!/usr/bin/env python
from flask import Flask, request, jsonify

import requests
import json
# import bson
import os
import Crypto
from Crypto.PublicKey import RSA
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AESCipher(object):

    def __init__(self, clientName): 
        self.bs = 32
        self.clientName = clientName
        self.key = clientName+'_AESKey'
        self.key = hashlib.sha256(self.key.encode()).digest()

    def saveKeyToFile(self):
        #'wb' open file as binary file so we can write the key(hashed bytes) to it
        with open(self.clientName+'_AESKey','wb') as f:
          f.write(self.key)

    def loadKeyfromFile(self):
        #'rb' open file as binary file so we can read the key (hashed bytes) as bytes
        with open(self.clientName+'_AESKey','wb') as f:
          key = f.read()
          return key

    def updateKey(self, newKey):
        self.key = newKey

    def getKey(self):
        return self.key

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

def loadOwnerPrivateKey():
    privKeyFile = open('owner_private_key.pem','r')
    strPrivKey = privKeyFile.read()
    loadedPrivKey = RSA.importKey(strPrivKey)
    privKeyFile.close()
    return loadedPrivKey

def loadOwnerPublicKey():
    pubKeyFile = open('owner_public_key.pem','r')
    strPubKey = pubKeyFile.read()
    loadedPubKey =  RSA.importKey(strPubKey)
    pubKeyFile.close()
    return loadedPubKey

def loadRequesterPublicKey():
    pubKeyFile = open('data_requester_public.pem','r')
    strPubKey = pubKeyFile.read()
    loadedPubKey =  RSA.importKey(strPubKey)
    pubKeyFile.close()
    return loadedPubKey

def generateKeyPair():
    key = RSA.generate(2048) #generate pub and priv key
    with open('owner_private_key.pem','w') as file:
        file.write(key.exportKey('PEM').decode())
    publickey = key.publickey() # pub key export for exchange
    with open('owner_public_key.pem','w') as file:
        file.write(publickey.exportKey('PEM').decode())

app = Flask(__name__) # create an instance of the Flask class

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done':False
    }
]

@app.route('/tasks', methods=['GET','POST'])
def get_tasks():
    if (request.method == 'GET'):
        return jsonify({'tasks': tasks})
    elif (request.method == 'POST'):
        data = request.data.decode()
        msgPkt = json.loads(data)
        encryptedAESKey = base64.decodestring(msgPkt['AESKey'].encode('utf-8'))
        ownerPrivKey = loadOwnerPrivateKey()
        AESKey = ownerPrivKey.decrypt(encryptedAESKey)
        ownerAESObj = AESCipher('data_owner')
        ownerAESObj.updateKey(AESKey)
        encryptedJsonMsg = msgPkt['payload'].encode('utf-8')
        jsonMsg = ownerAESObj.decrypt(encryptedJsonMsg)
        msg = json.loads(jsonMsg)
        if(msgPkt['type'] == 1):
            print(msg)
            # cmpstr(msg1['ownerSignedSourcePubKey'], ownerSignedSourcePubKey)
        elif(msgPkt['type'] == 2):
            signatureRTName = msg['signature']
            requesterPubKey = loadRequesterPublicKey()
            RT = msg['RT']
            name = RT['name']
            print(requesterPubKey.verify(name.encode(), signatureRTName))
            requesterPubKey = base64.decodestring(RT['requesterPublicKey'].encode())
            print(requesterPubKey)
        elif(msgPkt['type'] == 5):
            print(msg)
        return 'POST'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
